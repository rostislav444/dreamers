import io

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.db import models

from apps.attribute.abstract.fields import AttributeGroupTypeField
from apps.attribute.data.colors import colors
from apps.attribute.data.handles import handles
from apps.attribute.models import AttributeGroup, Attribute, AttributeSubGroup
from apps.category.models import Category
import os

from project.settings import MEDIA_ROOT


class Command(BaseCommand):
    subgroups = {
        'Dora': {
            'price': 180,
        },
        'Echo': {
            'price': 195,
        },
        'Miami': {
            'price': 184,
        },
        'Pirano': {
            'price': 209,
        },
        'Vivo': {
            'price': 220,
        },
    }

    def handle(self, *args, **options):
        attribute_group, _ = AttributeGroup.objects.get_or_create(
            name='Ткань',
            price_required=AttributeGroup.PRICE_RQ_SUB_GROUP,
            type=AttributeGroupTypeField.IMAGE,
            category=Category.objects.get(name='Диваны')
        )
        attribute_group.attributes.all().delete()

        for root, dirs, files in os.walk(os.path.join(MEDIA_ROOT, 'fabric'), topdown=False):
            for name in dirs:
                dir_path = os.path.join(root, name)
                sub_group, _ = AttributeSubGroup.objects.get_or_create(
                    group=attribute_group,
                    name=name,
                    price=self.subgroups[name]['price']
                )

                fabric_dir = os.path.join(MEDIA_ROOT, 'fabric/' + name)
                for d_root, d_dirs, d_files in os.walk(fabric_dir):
                    for f in d_files:
                        attribute, _ = Attribute.objects.get_or_create(value_image_image='/'.join(['fabric', name, f]),
                                                                       value_image_name=f.split('.')[0],
                                                                       attribute_group=attribute_group,
                                                                       sub_group=sub_group)
                        print(attribute.value_image_image)
