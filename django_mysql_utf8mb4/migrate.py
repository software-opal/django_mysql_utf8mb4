from django_mysql_utf8mb4.checks import get_preferred_collations
from django.db import connections


def db_colation_migration(connection, cursor=None):
    if connection.vendor != "mysql":
        return
    collation = get_preferred_collations(connection)[0]
    db_name = connection.get_connection_params()["db"]
    sql = "ALTER DATABASE %s CHARACTER SET utf8mb4 COLLATE %s;" % (db_name, collation)
    if cursor:
        cursor.execute(sql)
    else:
        with connection.cursor() as cursor:
            cursor.execute(sql)


def table_colation_migration(table_name, connection, cursor=None):
    if connection.vendor != "mysql":
        return
    collation = get_preferred_collations(connection)[0]
    sql = "ALTER TABLE %s CONVERT TO CHARACTER SET utf8mb4 COLLATE %s" % (
        table_name,
        collation,
    )
    try:
        if cursor:
            cursor.execute(sql)
        else:
            with connection.cursor() as cursor:
                cursor.execute(sql)
    except django.db.utils.ProgrammingError as e:
        if e.args[0] == 1146:
            # Table doesn't exist. Ignore it.
            pass
        else:
            raise


def django_tables_colation_migration(connection, cursor=None):
    if connection.vendor != "mysql":
        return
    for name in connection.introspection.django_table_names():
        table_colation_migration(name, connection, cursor=cursor)
