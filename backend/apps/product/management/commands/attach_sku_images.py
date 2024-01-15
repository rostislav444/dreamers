import os

from django.core.management.base import BaseCommand
from apps.product.models import Sku, SkuImages
from project.settings import MEDIA_ROOT


class Command(BaseCommand):
    def handle(self, *args, **options):
        dir_name = 'product/new_skuimages'
        dir_path = os.path.join(MEDIA_ROOT, 'product/new_skuimages')

        for sku_id in os.listdir(dir_path):
            sku_dir = os.path.join(dir_path, sku_id)

            sku = Sku.objects.filter(id=sku_id).first()
            sku.images.all().delete()

            for n, image in enumerate(os.listdir(sku_dir)):
                sku_image = SkuImages.objects.create(
                    sku=sku,
                    image=f'{dir_name}/{sku_id}/{image}',
                    index=n
                )

            print(sku_image.pk)
