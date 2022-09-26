import itertools

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.abstract.models import NameSlug
from apps.attribute.abstract.models import AttributeAbstract
from apps.attribute.models import AttributeGroup, Attribute
from apps.product.models import ProductClass


class Product(models.Model):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE)
    code = models.CharField(_('Code'), blank=True, null=True, max_length=255)
    price = models.PositiveIntegerField(_('Price'), blank=True, null=True)
    stock = models.PositiveIntegerField(_('Stock'), blank=True, null=True)
    model_3d = models.FileField(blank=True, null=True)
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

    def save(self, *args, **kwargs):
        self.generate_sku = True
        if self.generate_sku:
            self.generate_sku_from_options()
            self.generate_sku = False
        super(Product, self).save(*args, **kwargs)


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
    attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE)
    value_attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        unique_together = [
            ['attribute_group', 'value_attribute'],
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
        if self.attribute_group.type != 'attribute':
            self.value_attribute = None


class Sku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ', '.join([f'{sku_option.option.attribute_group.get_name}: {sku_option.option.get_name}' for sku_option
                          in self.options.all()])


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
    image = models.ImageField(upload_to='sku/')
    image_thumb = models.ImageField(upload_to='sku/', null=True, blank=True)
