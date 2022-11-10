import random
import string
import itertools

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.abstract.fields import CustomFileField, CustomImageField
from apps.abstract.models import NameSlug
from .models__productclass import ProductClass, ProductClassProductAttributes


class Product(NameSlug):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, related_name='products')
    code = models.CharField(_('Code'), blank=True, null=True, max_length=255)
    price = models.PositiveIntegerField(_('Price'), blank=True, null=True)
    stock = models.PositiveIntegerField(_('Stock'), blank=True, null=True)
    render_variants = models.BooleanField(default=False)
    generate_sku = models.BooleanField(default=False)

    def generate_sku_from_options(self):
        options_groups = [list(group.options.all()) for group in
                          self.product_class.option_groups.filter(image_dependency=True)]
        options_groups = itertools.product(*options_groups)

        for num, options_group in enumerate(options_groups):
            sku = Sku.objects.filter(product=self)
            for option in options_group:
                sku = sku.filter(options__option=option)
            if sku.count() == 0:
                sku = Sku.objects.create(product=self)
                for option in options_group:
                    SkuOptions.objects.create(sku=sku, option=option)
            print(num, sku)

    def __str__(self):
        return self.product_class.name

    @property
    def get_name(self):
        return '-'.join([self.product_class.name, self.code])

    def save(self, *args, **kwargs):
        if self.generate_sku:
            self.generate_sku_from_options()
            self.generate_sku = False
        super(Product, self).save(*args, **kwargs)


class Product3DBlenderModel(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='model_3d')
    blend = CustomFileField(validators=[FileExtensionValidator(allowed_extensions=["blend"])])
    blend1 = CustomFileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=["blend1"])])
    mtl = CustomFileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=["mtl"])])
    obj = CustomFileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=["obj"])])

    @property
    def get_name(self):
        return self.product.get_name + '_3d'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/')
    image_thumb = models.ImageField(upload_to='product/', null=True, blank=True)


class ProductProperty(NameSlug):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.value


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(ProductClassProductAttributes, on_delete=models.CASCADE,
                                  related_name='product_attributes', null=True, blank=True)
    # attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, related_name='product_attributes')
    # value_attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, blank=True, null=True,
    #                                     related_name='product_attributes')

    class Meta:
        unique_together = (('product', 'attribute'),)
        ordering = ('attribute',)

    @property
    def get_name(self):
        if self.attribute:
            return self.attribute
        return None


class Sku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sku')
    code = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ', '.join([f'{sku_option.option.attribute_group.get_name}: {sku_option.option.get_name}' for sku_option
                          in self.options.all()])

    @property
    def get_name(self):
        product = self.product.get_name
        options = '_'.join([f'{sku_option.option.attribute_group.get_name}-{sku_option.option.get_name}' for sku_option in self.options.all()])
        return '__'.join([product, options])


class SkuOptions(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, related_name='options')
    # option_group = models.ForeignKey('product.ProductClassOptionGroup', on_delete=models.PROTECT)
    option = models.ForeignKey('product.ProductClassOption', on_delete=models.PROTECT)

    class Meta:
        unique_together = (
            ('sku', 'option'),
        )
        ordering = ('sku', 'option')

    def __str__(self):
        return str(self.option.get_name)

    def validate(self, exclude=None):
        # TODO validate unique together option_group dynamically here and delete this field from model
        pass


class SkuImages(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, related_name='images')
    image = CustomImageField()
    image_thumb = CustomImageField(null=True, blank=True)
    index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('index',)

    def get_name(self):
        sku = self.sku.get_name
        sha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return '-'.join([sku, sha])

