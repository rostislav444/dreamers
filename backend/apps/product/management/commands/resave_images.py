import os

from django.core.management.base import BaseCommand
from apps.product.models import Sku, SkuImages, ProductPartSceneMaterialImage
from project.settings import MEDIA_ROOT


class Command(BaseCommand):
    def handle(self, *args, **options):
        for img in ProductPartSceneMaterialImage.objects.all():
            img.save()
            print(img.pk)

