import PIL
from PIL import ImageColor
from colorfield.fields import ColorField
from colorthief import ColorThief
from django.db import models

from apps.abstract.models import NameSlug
from apps.attribute.abstract.fields import AttributeGroupTypeField
from apps.attribute.abstract.models import AttributeGroupAbstract, AttributeAbstract
from apps.attribute.untils import get_closet_color
from apps.category.models import Category


class Colors(NameSlug):
    hex = ColorField(max_length=7)
    rgb = models.JSONField(default=list)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.rgb = PIL.ImageColor.getrgb(self.hex)
        super(Colors, self).save(*args, **kwargs)


# Units like: cm, kg.
class AttributeGroupUnit(NameSlug):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


# Ram, screen width...
class AttributeGroup(AttributeGroupAbstract):
    PRICE_RQ_SUB_GROUP = 'sub_group'
    PRICE_RQ_ATTRIBUTE = 'attribute'
    PRICE_RQ_MULTIPLIER = 'multiplier'
    PRICE_RQ_SUB_GROUP_MULTIPLIER = 'sub_group_multiplier'

    PRICE_REQUIRED_CHOICES = (
        (PRICE_RQ_SUB_GROUP, 'sub_group'),
        (PRICE_RQ_ATTRIBUTE, 'attribute'),
        (PRICE_RQ_MULTIPLIER, 'multiplier'),
        (PRICE_RQ_SUB_GROUP_MULTIPLIER, 'sub_group_multiplier'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attribute_groups', null=True,
                                 blank=True)
    unit = models.ForeignKey(AttributeGroupUnit, on_delete=models.PROTECT, blank=True, null=True)
    custom = models.BooleanField(default=False)
    price_required = models.CharField(default=None, max_length=20, null=True, blank=True,
                                      choices=PRICE_REQUIRED_CHOICES)

    def __str__(self):
        name_parts = [self.get_name, self.type, 'custom' if self.custom else '']
        return ', '.join(name_parts)

    @property
    def has_color(self):
        return self.type in [AttributeGroupTypeField.COLOR, AttributeGroupTypeField.IMAGE]


# Sometimes needed subgroups of attributes, like textile quality class
class AttributeSubGroup(NameSlug):
    group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, related_name='sub_groups')
    price = models.PositiveIntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class AttributeColor(models.Model):
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, related_name='attribute_colors')
    attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, related_name='colors')

    def __str__(self):
        return self.color.name


class Attribute(AttributeAbstract):
    attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, related_name='attributes')
    sub_group = models.ForeignKey(AttributeSubGroup, on_delete=models.PROTECT, blank=True, null=True)
    color = models.ForeignKey(AttributeColor, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='attributes')
    manual = models.BooleanField(default=False, editable=True)
    price = models.PositiveIntegerField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(AttributeAbstract, self).save(*args, **kwargs)
        if self.attribute_group.has_color:
            color_hex, color_rgb = None, None
            colors = Colors.objects.all()
            if self.attribute_group.type == AttributeGroupTypeField.COLOR:
                color_hex = self.value_color_hex
            elif self.attribute_group.type == AttributeGroupTypeField.IMAGE:
                try:
                    color_thief = ColorThief(self.value_image_image.path)
                    color_rgb = color_thief.get_color(quality=10)

                except PIL.UnidentifiedImageError:
                    return

            color = get_closet_color(color_hex, color_rgb, colors)
            if color:
                attribute_color, _ = AttributeColor.objects.get_or_create(color=color,
                                                                          attribute_group=self.attribute_group)
                self.color = attribute_color
            super(AttributeAbstract, self).save()


# Like clothes sizes values in different countries
class AttributeUnitGroup(NameSlug):
    STRING = 'string'
    INTEGER = 'integer'
    FLOAT = 'float'

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
