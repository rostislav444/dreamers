import abc

from django.db import models
from django.utils.html import mark_safe
from apps.abstract.models import NameSlug
from apps.attribute.abstract.models import AttributeGroupAbstract, AttributeAbstract
from apps.category.models import Category


# Units like: cm, kg.
class AttributeGroupUnit(NameSlug):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


# Ram, screen width...
class AttributeGroup(AttributeGroupAbstract):
    PRICE_RQ_SUB_GROUP = 'sub_group'
    PRICE_RQ_ATTRIBUTE = 'attribute'

    PRICE_REQUIRED_CHOICES = (
        (PRICE_RQ_SUB_GROUP, 'sub_group'),
        (PRICE_RQ_ATTRIBUTE, 'attribute')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attribute_groups', null=True,
                                 blank=True)
    unit = models.ForeignKey(AttributeGroupUnit, on_delete=models.PROTECT, blank=True, null=True)
    custom = models.BooleanField(default=False)
    price_required = models.CharField(default=None, max_length=9, null=True, blank=True, choices=PRICE_REQUIRED_CHOICES)

    def __str__(self):
        if self.custom:
            return f'{self.get_name} (custom)'
        return self.get_name


# Sometimes needed subgroups of attributes, like textile quality class
class AttributeSubGroup(NameSlug):
    group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE)


class Attribute(AttributeAbstract):
    group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, related_name='attributes')
    sub_group = models.ForeignKey(AttributeSubGroup, on_delete=models.PROTECT, blank=True, null=True)
    price = models.PositiveIntegerField(default=None, null=True, blank=True)

    def image_tag(self):
        path = None
        if self.value_image_image.path:
            path = self.value_image_image.name
        elif self.value_image_image.path:
            path = self.value_image_image.name
        if path:
            return mark_safe(f'''
                <img src="/media/{path}" width="80" height="80" style="
                    border: 1px solid #ccc; border-radius: 6px; margin-top: -4px; object-fit: cover
                " />
            ''')
        return None

    image_tag.short_description = 'Image'


# Like clothes sizes values in different countries
class AttributeUnitGroup(NameSlug):
    STRING = 'string'
    INTEGER = 'integer'
    FLOAT = 'FLOAT'

    CHOICES = (
        (STRING, 'String'),
        (INTEGER, 'Integer'),
        (FLOAT, 'Float')
    )

    group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, related_name='unit_group')
    type = models.CharField(max_length=255, choices=CHOICES, default=STRING)

    @property
    def actual_field_name(self):
        if self.type == self.STRING:
            return 'value_str'
        elif self.type == self.INTEGER:
            return 'value_int'
        elif self.type == self.FLOAT:
            return 'value_float'


class AttributeUnit(models.Model):
    unit = models.ForeignKey(AttributeUnitGroup, on_delete=models.PROTECT)
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT)
    value_str = models.SlugField(blank=True, null=True)
    value_int = models.PositiveIntegerField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = [
            ['unit', 'attribute'],
            ['unit', 'attribute', 'value_int'],
            ['unit', 'attribute', 'value_float'],
        ]
        ordering = (
            'attribute',
            'value_str',
            'value_int',
            'value_float',
        )

    def __str__(self):
        if self.unit == AttributeUnitGroup.STRING:
            return self.value_str
        elif self.unit == AttributeUnitGroup.INTEGER:
            return self.value_int
        elif self.unit == AttributeUnitGroup.FLOAT:
            return self.value_float
        else:
            return '-'

