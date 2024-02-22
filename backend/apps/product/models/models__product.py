import itertools
import random
import string

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.abstract.fields import DeletableImageField, DeletableFileField
from apps.abstract.models import NameSlug
from apps.attribute.models import AttributeGroup
from .models__productclass import ProductClass, ProductClassProductAttributes, ProductClassOptionGroup


class Product(models.Model):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, related_name='products')
    code = models.CharField(_('Code'), blank=True, null=True, max_length=255)
    price = models.PositiveIntegerField(_('Price'), blank=True, null=True)
    stock = models.PositiveIntegerField(_('Stock'), blank=True, null=True)
    render_variants = models.BooleanField(default=False)
    generate_sku = models.BooleanField(default=False, verbose_name='Сгенерировать SKU из материалов')

    width = models.PositiveIntegerField(_('Width'), default=0, blank=True)
    height = models.PositiveIntegerField(_('Height'), default=0, blank=True)
    depth = models.PositiveIntegerField(_('Depth'), default=0, blank=True)

    remove_images = models.BooleanField(default=False)

    class Meta:
        ordering = ['width', 'height', 'depth']

    def __str__(self):
        sku_count = self.sku.all().count()
        sku_with_images = self.sku.filter(images__isnull=False).distinct().count()
        return f'{self.product_class.name} ({str(sku_with_images)} / {str(sku_count)})'

    @property
    def get_image(self):
        sku = self.sku.filter(images__isnull=False).first()
        return sku.images.filter(index=0).first().image.url if sku else None

    @property
    def get_images(self):
        sku = self.sku.filter(images__isnull=False).first()
        return [obj.image.url for obj in sku.images.all()] if sku else None

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

    @property
    def get_name(self):
        return '-'.join([self.product_class.name, self.code])

    @property
    def get_price_multiplier_attribute_groups(self):
        return self.product_class.option_groups.filter(
            attribute_group__price_required=AttributeGroup.PRICE_RQ_MULTIPLIER)

    @property
    def get_price_sub_group_multiplier_attribute_groups(self):
        return self.product_class.option_groups.filter(
            attribute_group__price_required=AttributeGroup.PRICE_RQ_SUB_GROUP_MULTIPLIER)

    def save(self, *args, **kwargs):
        if self.generate_sku:
            self.generate_sku_from_options()
            self.generate_sku = False
        super(Product, self).save(*args, **kwargs)


class ProductCustomizedPart(models.Model):
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='customized_parts')
    part = models.ForeignKey('material.ProductPart', on_delete=models.PROTECT)
    area = models.DecimalField(default=1, decimal_places=1, max_digits=10)
    price = models.DecimalField(default=0, decimal_places=1, max_digits=10)

    def __str__(self):
        return str(self.part)


class Product3DBlenderModel(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='model_3d')
    obj = DeletableFileField(blank=True, null=True)
    mtl = DeletableFileField(blank=True, null=True)

    @property
    def get_name(self):
        return self.product.get_name + '_3d'


class Lights(models.Model):
    model_3d = models.ForeignKey(Product3DBlenderModel, on_delete=models.CASCADE, related_name='lights')
    power = models.IntegerField(default=1000)
    pos_x = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    pos_y = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    pos_z = models.DecimalField(default=0, max_digits=20, decimal_places=4)


class CameraLocations(models.Model):
    model_3d = models.ForeignKey(Product3DBlenderModel, on_delete=models.CASCADE, related_name='cameras')
    pos_x = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)
    pos_y = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)
    pos_z = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)
    rad_x = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)
    rad_y = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)
    rad_z = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/')
    image_thumb = models.ImageField(upload_to='product/', null=True, blank=True)


class ProductProperty(NameSlug):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.value


class ProductOptionPriceMultiplier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='multipliers')
    option_group = models.ForeignKey(ProductClassOptionGroup, on_delete=models.CASCADE, related_name='multiplier')
    value = models.PositiveIntegerField(default=0)


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(ProductClassProductAttributes, on_delete=models.CASCADE,
                                  related_name='product_attributes', null=True, blank=True)

    class Meta:
        unique_together = (('product', 'attribute'),)
        ordering = ('attribute__attribute_group',)

    @property
    def get_name(self):
        if self.attribute:
            return str(self.attribute)
        return None


class SkuPrefetchedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('materials', 'options', 'images').distinct()


class SkuManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Sku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sku')
    code = models.CharField(max_length=1024, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)

    objects_no_distinct = SkuManager()
    objects = SkuPrefetchedManager()

    class Meta:
        ordering = ['code']

    def __str__(self):
        img_count = str(self.images.count())
        return self.code + f' - imgs: {img_count}'

    @property
    def get_name(self):
        product = self.product.get_name
        options = '_'.join(
            [f'{sku_option.option.attribute_group.get_name}-{sku_option.option.get_name}' for sku_option in
             self.options.all()])
        return '__'.join([product, options])

    @property
    def get_code(self):
        materials = self.materials.all()
        return '__'.join([self.product.code, *[material.material.code for material in materials]])


class SkuMaterialsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('material__group__product_part').distinct()


class SkuMaterials(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey('material.ProductPartMaterials', on_delete=models.CASCADE,
                                 related_name='sku_materials')

    objects = SkuMaterialsManager()

    @property
    def get_material_part_name(self):
        return self.material.group.product_part.name


class SkuOptions(models.Model):
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, related_name='options')
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
    sku = models.ForeignKey(Sku, max_length=1024, on_delete=models.CASCADE, related_name='images')
    image = DeletableImageField()
    image_thumbnails = models.JSONField(default=dict, blank=True)
    index = models.PositiveIntegerField(default=0)
    local = models.BooleanField(default=False)

    class Meta:
        ordering = ('index',)

    def get_name(self):
        sku = self.sku.get_name
        sha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return '-'.join([sku, sha])
