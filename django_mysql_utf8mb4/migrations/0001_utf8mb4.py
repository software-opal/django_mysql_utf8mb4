from django.db import migrations
from django_mysql_utf8mb4.migrate import (
    db_colation_migration,
    django_tables_colation_migration,
)


def forwards_db_colation_migration(apps, schema_editor):
    if schema_editor.connection.vendor != "mysql":
        return
    # schema_editor acts as a cursor.
    db_colation_migration(schema_editor.connection, cursor=schema_editor)


def forwards_table_colation_migration(apps, schema_editor):
    if schema_editor.connection.vendor != "mysql":
        return
    # schema_editor acts as a cursor.
    django_tables_colation_migration(schema_editor.connection, cursor=schema_editor)


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(forwards_db_colation_migration, atomic=False),
        migrations.RunPython(forwards_table_colation_migration, atomic=False),
    ]
