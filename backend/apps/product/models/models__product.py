from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.abstract.models import NameSlug
from apps.attribute.models import AttributeGroupUnit, AttributeGroup, Attribute, PredefinedAttributeGroups
from apps.attribute.abstract.models import AttributeGroupAbstract, AttributeAbstract

from slugify import slugify


class Product(models.Model):
    product_class = models.ForeignKey('product.ProductClass', on_delete=models.CASCADE)
    code = models.CharField(_('Code'), blank=True, null=True, max_length=255)
    price = models.PositiveIntegerField(_('Price'), blank=True, null=True)
    stock = models.PositiveIntegerField(_('Stock'), blank=True, null=True)

    @property
    def get_required_attributes(self):
        categories = self.product_class.category.get_ancestors(include_self=True)
        attrs = PredefinedAttributeGroups.objects.filter(category__in=categories)
        return attrs

    def __str__(self):
        return self.product_class.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/')
    image_thumb = models.ImageField(upload_to='product/', null=True, blank=True)


class ProductProperty(NameSlug):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.value


class ProductAttribute(AttributeAbstract):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE)
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


# class ProductAttribute(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
#     attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.PROTECT)
#     attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, null=True, blank=True)

    # def __str__(self):
    #     return str(self.attribute_group.get_name) + ' - ' + str(self.attribute.get_name)


class Sku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)


class SkuOptions(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, related_name='options')
    option_group = models.ForeignKey('product.ProductClassOptionGroup', on_delete=models.PROTECT)
    option = models.ForeignKey('product.ProductClassOption', on_delete=models.PROTECT)

    class Meta:
        unique_together = (
            ('sku', 'option',),
        )
        ordering = ('sku', 'option',)

    def __str__(self):
        return str(self.option.get_name)

    def validate(self, exclude=None):
        pass

