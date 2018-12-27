from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Updates the database & table collations to the 'best' avaliable utf8mb4 collation"
    requires_migrations_checks = True

    def handle(self, *args, **kwargs):
        User = get_user_model()
        User.objects.filter(username=TEST_USERNAME).delete()
        try:
            user = User.objects.create_user(
                username=TEST_USERNAME,
                first_name="😀😀😀",
                last_name="😄😄😄",
                is_active=False,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    "User with extended unicode characters created successfully"
                )
            )
        except OperationalError as e:
            if e.args[0] == 1366:
                raise CommandError(
                    "Failed to create user using 4-byte UTF-8. Check the database colation."
                ) from e
            else:
                raise CommandError(
                    "Another error occurred whilst creating the user:\n  %s" % e
                ) from e
        finally:
            User.objects.filter(username=TEST_USERNAME).delete()
