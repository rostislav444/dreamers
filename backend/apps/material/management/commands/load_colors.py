import csv

from django.core.management.base import BaseCommand
from apps.material.models import Color
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Read and process data from ral_classic.csv'

    def handle(self, *args, **options):
        csv_file_path = 'data/ral_classic.csv'

        with open(csv_file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                try:
                    Color.objects.get(ral=row[0])
                except ObjectDoesNotExist:
                    color = Color(ral=row[0], rgb=row[1].split('-'), hex=row[2].lower(), name=row[5])
                    color.save()
