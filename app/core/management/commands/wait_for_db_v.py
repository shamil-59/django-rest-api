from django.core.management import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as PsycOpError
import time


class Command(BaseCommand):
    """Django command."""

    def handle(self, *args, **options) -> str | None:
        self.stdout.write("Waiting for db...")
        db_up = False
        while db_up is False: 
            try:   
                self.check(databases=['default'])
                db_up = True
            except (PsycOpError, OperationalError):
                self.stdout.write("Database not available, wait 2 seconds...")
                time.sleep(2)
        
        self.stdout.write(self.style.SUCCESS("Database available!!"))
    