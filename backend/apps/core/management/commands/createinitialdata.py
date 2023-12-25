import io
import os

import requests
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.db import models

from apps.attribute.abstract.fields import AttributeGroupTypeField
from apps.attribute.data.colors import colors
from apps.attribute.data.handles import handles
from apps.attribute.models import AttributeGroup, Attribute, AttributeColor
from apps.category.models import Category
from apps.core.colors import colors as web_colors
from project.settings import MEDIA_ROOT
from apps.material.models import Color


def get_file(path):
    url = 'http://localhost:8000/static/' + path
    name = path.split('/')[-1]
    response = requests.get(url)
    image = ImageFile(io.BytesIO(response.content), name=name)
    return image


def get_fabric_data():
    for root, dirs, files in os.walk(os.path.join(MEDIA_ROOT, 'fabric'), topdown=False):
        for name in dirs:
            print(os.path.join(root, name))
    pass


def add_base_colors():
    AttributeColor.objects.all().delete()
    Color.objects.all().delete()

    for base_color in web_colors:
        color, _ = Color.objects.get_or_create(name=base_color['name'], hex=base_color['hex'])
        print(color)


models_data = {
    'Attribute': {
        'model': Attribute,
        'fk_name': 'attribute_group'
    },
    'Category': {
        'model': Category,
        'fk_name': 'parent',
    },
    'AttributeGroup': {
        'model': AttributeGroup,
        'fk_name': 'category',
    }

}


class Command(BaseCommand):

    @property
    def data(self):
        return [{
            **models_data['Category'],
            'data': [{
                'name': 'Мебель',
                'parent': None,
                'children': [{
                    **models_data['Category'],
                    'data': [
                        {'name': 'Тумбы под медиа'},
                        {'name': 'Шкафы', 'children': [{
                            **models_data['AttributeGroup'],
                            'data': [{
                                'name': 'Цвет фасадов',
                                'type': AttributeGroupTypeField.COLOR,
                                'price_required': AttributeGroup.PRICE_RQ_ATTRIBUTE,
                                'children': [{
                                    **models_data['Attribute'],
                                    'data': [{'value_color_name': name, 'value_color_hex': color_hex} for
                                             name, color_hex in colors.items()]
                                }]}
                            ]}, {
                            **models_data['AttributeGroup'],
                            'data': [{
                                'name': 'Ширина',
                                'type': AttributeGroupTypeField.INTEGER,
                                'price_required': None,
                                'children': [{
                                    **models_data['Attribute'],
                                    'data': [{'value_integer': num} for num in [120, 140, 160, 180, 200, 220, 240]]
                                }]}
                            ]}, {
                            **models_data['AttributeGroup'],
                            'data': [{
                                'name': 'Высота',
                                'type': AttributeGroupTypeField.INTEGER,
                                'price_required': None,
                                'children': [{
                                    **models_data['Attribute'],
                                    'data': [{'value_integer': num} for num in [40, 60, 80, 100, 120]]
                                }]}
                            ]},
                        ]},
                        {
                            'name': 'Диваны',
                            'children': {
                                **models_data['AttributeGroup'],
                                'data': [{
                                    'name': 'Ткань',
                                    'type': AttributeGroupTypeField.IMAGE,
                                    'price_required': None,
                                    'children': [{
                                        **models_data['Attribute'],
                                        'data': get_fabric_data(),
                                    }]}
                                ]},

                        },
                        {'name': 'Кровати'},
                        {'name': 'Стулья'},
                    ]
                }, {
                    **models_data['AttributeGroup'],
                    'fk_name': 'category',
                    'data': [{
                        'name': 'Цвет корпуса',
                        'type': AttributeGroupTypeField.COLOR,
                        'children': [{
                            **models_data['Attribute'],
                            'data': [{'value_color_name': key, 'value_color_hex': value} for key, value in
                                     colors.items()]
                        }]
                    }, {
                        'name': 'Ручки',
                        'type': AttributeGroupTypeField.IMAGE,
                        'children': [{
                            **models_data['Attribute'],
                            'data': [{'value_image_image': get_file(item['image']), 'value_image_name': item['name'],
                                      'price': item.get('price')} for item in handles]
                        }]
                    }]
                }]
            }]
        }]


    def handle(self, *args, **options):
        add_base_colors()
        get_fabric_data()

        def get_model_image_fields(model):
            fields = []
            # Exclude image fields from search
            for field in model._meta.get_fields():
                if models.ImageField in field.__class__.__bases__:
                    fields.append(field.name)
            return fields

        def get_or_save_item(model, data, exclude_fields_from_search):
            try:
                _data = {k: v for k, v in data.items() if k not in exclude_fields_from_search}
                print(model, _data)
                item = model.objects.get(**_data)
            except ObjectDoesNotExist:
                item = model(**data)
                item.save()
            return item

        def recursive_loop(main_data, parent=None):
            if type(main_data) == list:
                for obj in main_data:
                    model = obj['model']
                    exclude_fields_from_search = get_model_image_fields(model)
                    if type(obj['data']) != list:
                        raise ValidationError('Object data should be list')
                    for data in obj['data']:
                        children = data.pop('children', None)
                        if parent:
                            data[obj['fk_name']] = parent
                        item = get_or_save_item(model, data, exclude_fields_from_search)
                        if children:
                            recursive_loop(children, item)
            return None

        recursive_loop(self.data)
