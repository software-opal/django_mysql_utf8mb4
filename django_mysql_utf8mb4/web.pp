class matomo3::web {
  include matomo3::php

  file { '/var/log/matomo/www/':
    ensure  => directory,
    owner   => 'www-data',
    group   => 'adm',
    mode    => '0755',
    require => [
      Package['nginx-full'],
      File['/var/log/matomo/'],
    ],
  }
  -> file { '/etc/logrotate.d/matomo-www':
    ensure => present,
    source => "puppet:///modules/${module_name}/etc/logrotate.d/matomo-www",
    owner  => 'root',
    group  => 'root',
    mode   => '0644',
  }

  class { 'nginx':
    package => 'nginx-full',
  }
  file { '/etc/nginx/sites-enabled/default':
    ensure => absent,
  }

  file { '/etc/nginx/sites-available/matomo.conf':
    ensure  => present,
    source  => "puppet:///modules/${module_name}/etc/nginx/sites-available/matomo.conf",
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    require => [File['/var/log/matomo/www/']],
  }
  -> file { '/etc/nginx/sites-enabled/matomo.conf':
    ensure => link,
    target => '/etc/nginx/sites-available/matomo.conf',
  }

  class { 'nginx::fastcgi':
    intercept_errors => 'off',
  }

  augeas { 'configure fpm/php.ini memory limit':
    require => Package['php'],
    context => '/files/etc/php/7.2/fpm/php.ini',
    changes => [
      'set PHP/memory_limit 1024M',
    ],
  }

  package { 'php7.2-fpm':
    ensure => present,
  }
  -> file { '/etc/php/7.2/fpm/pool.d/www.conf':
    ensure  => absent,
  }
  -> file { '/etc/php/7.2/fpm/pool.d/matomo.conf':
    ensure  => present,
    source  => "puppet:///modules/${module_name}/etc/php/7.2/fpm/pool.d/matomo.conf",
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    require => [File['/var/log/matomo/php/']],
    notify  => [Service['php7.2-fpm']],
  }
  -> service { 'php7.2-fpm':
    ensure => running,
    enable => true,
  }
}
