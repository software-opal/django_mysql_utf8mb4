from django.core.checks import register, Tags, Error
from django.db import connections


PREFERED_COLLATIONS = (
    "utf8mb4_unicode_520_ci",
    "utf8mb4_unicode_520_ci",
    "utf8mb4_general_ci",
    "utf8mb4_unicode_ci",
)

E001_DB_COLLATE_MESSAGE = "Database %s uses a bad collation(%s)."
E001_DB_COLLATE_HINT = "ALTER DATABASE %s COLLATE %s;"
W001_DB_COLLATE_MESSAGE = "Database %s uses a valid, but not-preferred collation(%s)."
W001_DB_COLLATE_HINT = "ALTER DATABASE %s COLLATE %s;"

E002_TABLE_COLLATE_MESSAGE = "Table %s.%s uses a bad collation(%s)."
E002_TABLE_COLLATE_HINT = "USE %s; ALTER TABLE %s COLLATE %s;"
W002_TABLE_COLLATE_MESSAGE = (
    "Table %s.%s uses a valid, but not-preferred collation(%s)."
)
W002_TABLE_COLLATE_HINT = "USE %s; ALTER TABLE %s COLLATE %s;"


def get_utf8mb_collations(connection):
    with connection.cursor() as cursor:
        cursor.execute("SHOW COLLATION WHERE Charset='utf8mb4';")
        return frozenset([row[0] for row in cursor.fetchall()])


def get_preferred_collations(connection):
    valid_collations = get_utf8mb_collations(connection)
    return [
        collation for collation in PREFERED_COLLATIONS if collation in valid_collations
    ]


@register(Tags.database)
def check_utf8mb4_database(app_configs, **kwargs):
    errors = []
    for connection in connections.all():
        if connection.vendor != "mysql":
            continue
        db_name = connection.get_connection_params()["db"]
        valid_collations = get_utf8mb_collations(connection)
        preferred_collations = [c for c in PREFERED_COLLATIONS if c in valid_collations]
        with connection.cursor() as cursor:
            cursor.execute("SELECT @@collation_database;")
            collation, = cursor.fetchone()
        if collation not in valid_collations:
            errors.append(
                Error(
                    E001_DB_COLLATE_MESSAGE % (connection.alias, collation),
                    hint=E001_DB_COLLATE_HINT % (db_name, preferred_collations[0]),
                    id="tiaki.base.E001",
                )
            )
        elif collation not in preferred_collations:
            errors.append(
                Warning(
                    W001_DB_COLLATE_MESSAGE % (connection.alias, collation),
                    hint=W001_DB_COLLATE_HINT % (db_name, preferred_collations[0]),
                    id="tiaki.base.W001",
                )
            )
    return errors


@register(Tags.models)
def check_utf8mb_collation(app_configs, **kwargs):
    errors = []
    for connection in connections.all():
        if connection.vendor != "mysql":
            continue
        tables = connection.introspection.django_table_names()
        db_name = connection.get_connection_params()["db"]
        valid_collations = get_utf8mb_collations(connection)
        preferred_collations = [c for c in PREFERED_COLLATIONS if c in valid_collations]
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT TABLE_NAME, TABLE_COLLATION FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=%s;",
                (db_name,),
            )
            table_collations = [
                (table, collation) for table, collation in cursor if table in tables
            ]
        for table, collation in table_collations:
            if collation not in valid_collations:
                errors.append(
                    Error(
                        E002_TABLE_COLLATE_MESSAGE
                        % (connection.alias, table, collation),
                        hint=E002_TABLE_COLLATE_HINT
                        % (db_name, table, preferred_collations[0]),
                        id="tiaki.base.E002",
                    )
                )
            elif collation not in preferred_collations:
                errors.append(
                    Warning(
                        W002_TABLE_COLLATE_MESSAGE
                        % (connection.alias, table, collation),
                        hint=W002_TABLE_COLLATE_HINT
                        % (db_name, table, preferred_collations[0]),
                        id="tiaki.base.W002",
                    )
                )
    return errors
