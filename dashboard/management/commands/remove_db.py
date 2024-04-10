import os

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        paths = [
            'dashboard/migrations/',
            'users/migrations/',
        ]
        for path in paths:
            abs_path = os.path.abspath(path)
            for filename in os.listdir(abs_path):
                if filename.startswith('00'):
                    os.remove(os.path.join(abs_path, filename))
        os.remove('db.sqlite3')
