from django.core.management.base import BaseCommand, CommandError
from apps.attribute.models import AttributeGroup, Attribute
from apps.attribute.data.colors import colors


class Command(BaseCommand):
    def handle(self, *args, **options):
        color_attr_group, created_attr_group = AttributeGroup.objects.get_or_create(type='color', name="Paint color")
        for k, v in colors.items():
            color_attr, created_attr = Attribute.objects.get_or_create(group=color_attr_group, value_color_name=k,
                                                                       value_color_hex=v)
            print(color_attr.value_color_name)
