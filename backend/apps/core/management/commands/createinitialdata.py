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
from apps.attribute.models import AttributeGroup, Attribute
from apps.category.models import Category


def get_file(path):
    url = 'http://localhost:8000/static/' + path
    name = path.split('/')[-1]
    response = requests.get(url)
    image = ImageFile(io.BytesIO(response.content), name=name)
    return image


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    @property
    def data(self):
        return [{
            'model': Category,
            'fk_name': 'parent',
            'data': [{
                'name': 'Мебель',
                'parent': None,
                'children': [{
                    'model': Category,
                    'fk_name': 'parent',
                    'data': [
                        {'name': 'Тумбы под медиа'},
                        {'name': 'Шкафы', 'children': [{
                            'model': AttributeGroup,
                            'fk_name': 'category',
                            'data': [{
                                'name': 'Цвет фасадов',
                                'type': AttributeGroupTypeField.COLOR,
                                'price_required': AttributeGroup.PRICE_RQ_ATTRIBUTE,
                                'children': [{
                                    'model': Attribute,
                                    'fk_name': 'group',
                                    'data': [{'value_color_name': name, 'value_color_hex': color_hex} for
                                             name, color_hex in colors.items()]
                                }]}
                            ]}
                        ]},
                        {'name': 'Диваны'},
                        {'name': 'Кровати'},
                        {'name': 'Стулья'},
                    ]
                }, {
                    'model': AttributeGroup,
                    'fk_name': 'category',
                    'data': [{
                        'name': 'Цвет корпуса',
                        'type': AttributeGroupTypeField.COLOR,
                        'children': [{
                            'model': Attribute,
                            'fk_name': 'group',
                            'data': [{'value_color_name': key, 'value_color_hex': value} for key, value in
                                     colors.items()]
                        }]
                    }, {
                        'name': 'Ручки',
                        'type': AttributeGroupTypeField.IMAGE,
                        'children': [{
                            'model': Attribute,
                            'fk_name': 'group',
                            'data': [{'value_image_image': get_file(item['image']), 'value_image_name': item['name'],
                                      'price': item.get('price')} for item in handles]
                        }]
                    }]
                }]
            }]
        }]

    def handle(self, *args, **options):
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
