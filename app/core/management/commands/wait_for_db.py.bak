"""
Django command to wait for the database to be availeble.
"""

from psycopg2 import OperationalError as PsycOpError
from django.db.utils import OperationalError
from django.core.management import BaseCommand
import time


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options) -> str | None:
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycOpError, OperationalError):
                self.stdout.write('Database unavailable, wait 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!!!'))
