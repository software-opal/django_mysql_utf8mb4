from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError
from django.db import connections

from django_mysql_utf8mb4.migrate import (
    db_colation_migration,
    django_tables_colation_migration,
)


class Command(BaseCommand):
    help = "Updates the database & table collations to the 'best' avaliable utf8mb4 collation"
    requires_migrations_checks = True

    def handle(self, *args, **kwargs):
        for connection in connections.all():
            db_colation_migration(connection)
            django_tables_colation_migration(connection)
