from django.db import models
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from apps.abstract.models import NameSlug
from apps.attribute.abstract import AttributeImageField
from apps.attribute.abstract.fields import AttributeGroupTypeField
from slugify import slugify
import abc


class AttributeGroupAbstract(NameSlug):
    type = AttributeGroupTypeField(max_length=24)
    __type = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(AttributeGroupAbstract, self).__init__( *args, **kwargs)
        self.__type = self.type

    def save(self, *args, **kwargs):
        super(AttributeGroupAbstract, self).save(*args, **kwargs)
        self.__type = self.type

    @property
    @abc.abstractmethod
    def unit(self):
        pass

    @property
    def attr_fields(self):
        return {
            AttributeGroupTypeField.TEXT: 'value_text',
            AttributeGroupTypeField.INTEGER: 'value_integer',
            AttributeGroupTypeField.BOOLEAN: 'value_boolean',
            AttributeGroupTypeField.FLOAT: 'value_float',
            AttributeGroupTypeField.COLOR: ['value_color_name', 'value_color_hex', 'value_color_image'],
            AttributeGroupTypeField.RANGE: ['value_min', 'value_max'],
            AttributeGroupTypeField.IMAGE: ['value_image_name', 'value_image_image']
        }

    @property
    def actual_field_name(self):
        return self.attr_fields[self.type]


class AttributeAbstract(models.Model):
    value_text = models.CharField(_('Text'), max_length=500, blank=True, null=True)
    value_integer = models.IntegerField(_('Integer'), blank=True, null=True, db_index=True)
    value_boolean = models.BooleanField(_('Boolean'), blank=True, null=True, db_index=True)
    value_float = models.FloatField(_('Float'), blank=True, null=True, db_index=True)
    value_color_name = models.CharField(_('Color'), max_length=500, blank=True, null=True)
    value_color_hex = ColorField(_('Color HEX'), max_length=7, blank=True, null=True)
    value_color_image = AttributeImageField(_('Color IMAGE'), blank=True, null=True)
    value_image_name = models.CharField(_('Name'), max_length=500, blank=True, null=True)
    value_image_image = AttributeImageField(_('Image'), max_length=500, blank=True, null=True)
    value_min = models.IntegerField(_('Min'), blank=True, null=True, db_index=True)
    value_max = models.IntegerField(_('Max'), blank=True, null=True, db_index=True)
    slug = models.SlugField(max_length=1024, blank=True, null=True, editable=False)

    class Meta:
        abstract = True
        unique_together = [
            ['group', 'value_text'],
            ['group', 'value_integer'],
            ['group', 'value_boolean'],
            ['group', 'value_float'],
            ['group', 'value_color_name', 'value_color_hex', 'value_color_image'],
            ['group', 'value_min', 'value_max'],
        ]
        ordering = (
            'value_text',
            'value_integer',
            'value_boolean',
            'value_float',
            'value_color_name',
            'value_min',
            'value_max',
            'value_image_name'
        )

    @property
    @abc.abstractmethod
    def group(self):
        pass

    @property
    def get_attribute_name(self):
        group = self.group
        if group.type == AttributeGroupTypeField.RANGE:
            return str(self.value_min) + ' - ' + str(self.value_max)
        elif group.type == AttributeGroupTypeField.COLOR:
            return self.value_color_name
        elif group.type == AttributeGroupTypeField.IMAGE:
            return self.value_image_name
        return getattr(self, self.group.actual_field_name)

    @property
    def get_name(self):
        return self.get_attribute_name

    def __str__(self):
        return str(self.get_name)

    def value(self):
        group = self.group
        if group.type == AttributeGroupTypeField.RANGE:
            return {
                'min': self.value_min,
                'max': self.value_max
            }
        if group.type == AttributeGroupTypeField.COLOR:
            return {
                'name': self.value_color_name,
                'hex': self.value_color_hex,
                'image': self.value_color_image.path,
            }
        if group.type == AttributeGroupTypeField.IMAGE:
            return {
                'name': self.value_image_name,
                'image': self.value_image_image.path
            }
        return getattr(self, self.group.actual_field_name)

    @property
    def get_slug(self):
        group = self.group
        values = [self.group.slug]
        if group.type == AttributeGroupTypeField.RANGE:
            values.append('min-' + str(self.value_min))
            values.append('max-' + str(self.value_max))
        elif group.type == AttributeGroupTypeField.COLOR:
            values.append(self.value_color_name)
        elif group.type == AttributeGroupTypeField.IMAGE:
            values.append(self.value_image_name)
        else:
            values.append(getattr(self, group.actual_field_name))
        values = [str(value) for value in values]
        return slugify('-'.join(values))

    def validator(self):
        if self.group.type == AttributeGroupTypeField.RANGE and self.value_min >= self.value_max:
            raise ValueError('MIN value cant be bigger or equal MAX')

    def save(self, *args, **kwargs):
        self.validator()
        self.slug = self.get_slug
        super(AttributeAbstract, self).save(*args, **kwargs)