import os

from django.core.management.base import BaseCommand
from apps.product.models import Sku, SkuImages
from project.settings import MEDIA_ROOT


class Command(BaseCommand):
    def handle(self, *args, **options):
        dir_path = os.path.join(MEDIA_ROOT, 'product/skuimages')

        for sku_dir in os.listdir(dir_path):
            image_file = os.path.join('product/skuimages', sku_dir, 'image.png')

            sku = Sku.objects.filter(id=sku_dir).first()

            sku_image = SkuImages.objects.create(
                sku=sku,
                image=image_file,
                image_thumbnails={
                    'l': image_file,
                    'm': image_file,
                    's': image_file
                })

            print(sku_image.pk)
