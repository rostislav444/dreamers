import abc

from colorfield.fields import ColorField
from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify import slugify

from apps.abstract.models import NameSlug
from apps.attribute.abstract import AttributeImageField
from apps.attribute.abstract.fields import AttributeGroupTypeField


class AttributeGroupAbstract(NameSlug):
    type = AttributeGroupTypeField(max_length=24)
    __type = None

    class Meta:
        abstract = True
        ordering = ['type', 'name']

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
            AttributeGroupTypeField.TEXT: ['value_text'],
            AttributeGroupTypeField.INTEGER: ['value_integer'],
            AttributeGroupTypeField.BOOLEAN: ['value_boolean'],
            AttributeGroupTypeField.FLOAT: ['value_float'],
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
            ['attribute_group', 'value_text'],
            ['attribute_group', 'value_integer'],
            ['attribute_group', 'value_boolean'],
            ['attribute_group', 'value_float'],
            ['attribute_group', 'value_color_name', 'value_color_hex', 'value_color_image'],
            ['attribute_group', 'value_min', 'value_max'],
        ]
        ordering = (
            'value_text',
            'value_integer',
            'value_boolean',
            'value_float',
            'value_color_hex',
            'value_min',
            'value_max',
            'value_image_name'
        )

    @property
    @abc.abstractmethod
    def attribute_group(self):
        pass

    @property
    def get_attribute_name(self):
        attribute_group = self.attribute_group
        if attribute_group.type == AttributeGroupTypeField.RANGE:
            return str(self.value_min) + ' - ' + str(self.value_max)
        elif attribute_group.type == AttributeGroupTypeField.COLOR:
            return self.value_color_name
        elif attribute_group.type == AttributeGroupTypeField.IMAGE:
            return self.value_image_name
        return getattr(self, self.attribute_group.actual_field_name[0])

    def __str__(self):
        return str(self.get_name)

    @property
    def get_name(self):
        return self.get_attribute_name

    @property
    def get_value(self):
        attribute_group = self.attribute_group
        if attribute_group.type == AttributeGroupTypeField.RANGE:
            return {
                'min': self.value_min,
                'max': self.value_max
            }
        if attribute_group.type == AttributeGroupTypeField.COLOR:
            return {
                'name': self.value_color_name,
                'hex': self.value_color_hex,
                'image': self.value_color_image.name if self.value_color_image else None
            }
        if attribute_group.type == AttributeGroupTypeField.IMAGE:
            return {
                'name': self.value_image_name,
                'image': self.value_image_image.name if self.value_image_image else None
            }
        return getattr(self, self.attribute_group.actual_field_name[0])

    @property
    def value(self):
        return self.get_value

    @property
    def get_slug(self):
        attribute_group = self.attribute_group
        values = [self.attribute_group.slug]
        if attribute_group.type == AttributeGroupTypeField.RANGE:
            values.append('min-' + str(self.value_min))
            values.append('max-' + str(self.value_max))
        elif attribute_group.type == AttributeGroupTypeField.COLOR:
            values.append(self.value_color_name)
        elif attribute_group.type == AttributeGroupTypeField.IMAGE:
            values.append(self.value_image_name)
        else:
            values += attribute_group.actual_field_name
        values = [str(value) for value in values]
        return slugify('-'.join(values))

    def validator(self):
        empty = True
        for field in self.attribute_group.actual_field_name:
            if getattr(self, field):
                empty = False
                break
        if empty:
            raise ValueError('Form is empty')

        if self.attribute_group.type == AttributeGroupTypeField.RANGE:
            if not self.value_min:
                raise ValueError('MIN value cant be null')
            if self.value_min >= self.value_max:
                raise ValueError('MIN value cant be bigger or equal MAX')

    # TODO Make able to first save attribute group and only then validate
    def save(self, *args, **kwargs):
        self.validator()
        self.slug = self.get_slug
        super(AttributeAbstract, self).save(*args, **kwargs)


class AttributeAbstractWithValueAttribute(AttributeAbstract):
    value_attribute = models.ForeignKey('attribute.Attribute', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        abstract = True
        unique_together = [
            ['attribute_group', 'value_attribute'],
            *AttributeAbstract.Meta.unique_together
        ]
        ordering = (
            'value_attribute',
            *AttributeAbstract.Meta.ordering,
        )

    @property
    @abc.abstractmethod
    def attribute_group(self):
        pass

    @property
    def get_name(self):
        if self.value_attribute:
            return self.value_attribute.get_attribute_name
        return self.get_attribute_name

    @property
    def value(self):
        if self.attribute_group.type == 'attribute':
            return self.value_attribute.value
        return self.get_value

    def validator(self):
        if self.attribute_group.type != 'attribute':
            self.value_attribute = None
