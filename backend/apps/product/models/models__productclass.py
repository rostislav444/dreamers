from django.db import models
from apps.abstract.models import NameSlug
from apps.category.models import Category, Properties
from apps.attribute.models import AttributeGroupUnit, AttributeGroup, Attribute
from apps.attribute.abstract.models import AttributeGroupAbstract, AttributeAbstract
from apps.attribute.abstract.fields import ProductOptionGroupField
from slugify import slugify


class ProductClass(NameSlug):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return self.name


# Create your models here.
class ProductClassProperty(NameSlug):
    product = models.ForeignKey(ProductClass, on_delete=models.CASCADE, related_name='properties')
    property = models.ForeignKey(Properties, on_delete=models.PROTECT)

    def get_slug(self):
        return slugify(self.property.name + '-' + self.name)

    def __str__(self):
        return self.property.name + ' - ' + self.name


# Attribute option
class ProductClassOptionGroup(AttributeGroupAbstract):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    type = ProductOptionGroupField(max_length=24)
    attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='product_class_option_group')
    unit = models.ForeignKey(AttributeGroupUnit, on_delete=models.PROTECT, blank=True, null=True)
    save_all_options = models.BooleanField(default=True)

    def __str__(self):
        name = self.get_name
        if name:
            return name
        return '-'

    @property
    def get_name(self):
        if self.attribute_group:
            if self.attribute_group:
                return self.attribute_group.name
            else:
                return None
        return self.name

    @property
    def actual_field_name(self):
        attr_fields = {
            ProductOptionGroupField.ATTRIBUTE: 'value_attribute',
            **self.attr_fields,
        }
        return attr_fields[self.type]

    def validate(self):
        if self.type == ProductOptionGroupField.ATTRIBUTE:
            self.unit = None
            self.name = None
        else:
            self.attribute_group = None

    def save(self, *args, **kwargs):
        super(ProductClassOptionGroup, self).save(*args, **kwargs)


class ProductClassOption(AttributeAbstract):
    group = models.ForeignKey(ProductClassOptionGroup, on_delete=models.CASCADE)
    value_attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        unique_together = [
            ['group', 'value_attribute'],
            *AttributeAbstract.Meta.unique_together
        ]
        ordering = (
            'value_attribute',
            *AttributeAbstract.Meta.ordering,
        )

    @property
    def get_name(self):
        if self.value_attribute:
            return self.value_attribute.get_attribute_name
        return self.get_attribute_name

    def validator(self):
        if self.group.type != 'attribute':
            self.value_attribute = None

    def save(self, *args, **kwargs):
        super(ProductClassOption, self).save(*args, **kwargs)


class ProductAttributeOptionImage(models.Model):
    product_option = models.ForeignKey(ProductClassOption, on_delete=models.CASCADE)
    image = models.ImageField()


