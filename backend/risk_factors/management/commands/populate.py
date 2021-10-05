import csv
import os

from django.core.management.base import BaseCommand
from risk_factors.models import Disease
from backend.settings import BASE_DIR


def populate_diseases(path):
    file_path = os.path.join(BASE_DIR, path)
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            Disease.objects.create(illness=row[0], description=row[1])


class Command(BaseCommand):
    help = 'Populates database with disease data.'

    def handle(self, *args, **options):
        entities = {
            'diseases': {
                'path': 'risk_factors/management/commands/data/diseases.csv',
                'method': populate_diseases
            },
        }

        for entity, metadata in entities.items():
            metadata['method'](metadata['path'])
            message = f"Successfully populated databases with {entity}."
            self.stdout.write(self.style.SUCCESS(message))
