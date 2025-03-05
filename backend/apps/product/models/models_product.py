import random
import string

from apps.abstract.fields import DeletableImageField
from apps.abstract.models import NameSlug
from apps.attribute.models import AttributeGroup
from django.db import models
from django.utils.translation import gettext_lazy as _

from .models_3d import Camera
from .models_productclass import (
    ProductClass,
    ProductClassOptionGroup,
    ProductClassProductAttributes,
)


class Product(models.Model):
    product_class = models.ForeignKey(
        ProductClass, on_delete=models.CASCADE, related_name="products"
    )
    code = models.CharField(_("Code"), blank=True, null=True, max_length=255)
    price = models.PositiveIntegerField(_("Price"), blank=True, null=True)
    stock = models.PositiveIntegerField(_("Stock"), blank=True, null=True)
    render_variants = models.BooleanField(default=False)

    generate_sku_from_materials = models.BooleanField(
        default=False, verbose_name="Сгенерировать SKU из материалов"
    )

    width = models.PositiveIntegerField(_("Width"), default=0, blank=True)
    height = models.PositiveIntegerField(_("Height"), default=0, blank=True)
    depth = models.PositiveIntegerField(_("Depth"), default=0, blank=True)

    remove_images = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Вариант"
        verbose_name_plural = "2. Варианты"
        ordering = ["product_class", "width", "height", "depth"]

    def __str__(self):
        return self.product_class.name

    @property
    def get_image(self):
        sku = self.skus.filter(images__isnull=False).first()
        return sku.images.filter(index=0).first().image.url if sku else None

    @property
    def get_sku_images(self):
        sku = self.skus.filter(images__isnull=False).first()
        return [obj.image.url for obj in sku.images.all()] if sku else None

    @property
    def get_parts_images(self):
        links = []
        model_3d = self.model_3d.first()
        if model_3d:
            try:
                camera = model_3d.cameras.get(rad_z=90)
            except Camera.DoesNotExist:
                camera = model_3d.cameras.filter(rad_z__gte=70, rad_z__lte=100).first()
            if not camera:
                camera = model_3d.cameras.first()
            if camera:
                for part in camera.parts.all():
                    material = part.materials.first()
                    if hasattr(material, "image"):
                        links.append(material.image.image.name)
        return links

    @property
    def get_name(self):
        return "-".join([self.product_class.name, self.code])

    @property
    def get_price_multiplier_attribute_groups(self):
        return self.product_class.option_groups.filter(
            attribute_group__price_required=AttributeGroup.PRICE_RQ_MULTIPLIER
        )

    @property
    def get_price_sub_group_multiplier_attribute_groups(self):
        return self.product_class.option_groups.filter(
            attribute_group__price_required=AttributeGroup.PRICE_RQ_SUB_GROUP_MULTIPLIER
        )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="product/")
    image_thumb = models.ImageField(upload_to="product/", null=True, blank=True)


class ProductProperty(NameSlug):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name + " - " + self.value


class ProductOptionPriceMultiplier(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="multipliers"
    )
    option_group = models.ForeignKey(
        ProductClassOptionGroup, on_delete=models.CASCADE, related_name="multiplier"
    )
    value = models.PositiveIntegerField(default=0)


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes"
    )
    attribute = models.ForeignKey(
        ProductClassProductAttributes,
        on_delete=models.CASCADE,
        related_name="product_attributes",
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = (("product", "attribute"),)
        ordering = ("attribute__attribute_group",)

    @property
    def get_name(self):
        if self.attribute:
            return str(self.attribute)
        return None


class Sku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="skus")
    code = models.CharField(max_length=1024, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    materials = models.ManyToManyField(
        "material.ProductPartMaterials", related_name="sku_materials"
    )
    generate_images = models.BooleanField(default=True)


class SkuImages(models.Model):
    sku = models.ForeignKey(
        Sku, max_length=1024, on_delete=models.CASCADE, related_name="images"
    )
    camera = models.ForeignKey(
        Camera,
        on_delete=models.CASCADE,
        related_name="sku_images",
        null=True,
        blank=True,
    )
    image = DeletableImageField(null=True, blank=True)
    image_thumbnails = models.JSONField(default=dict, blank=True)
    index = models.PositiveIntegerField(default=0)
    local = models.BooleanField(default=False)

    class Meta:
        ordering = ("index",)

    @property
    def name(self):
        return self.get_name()

    def get_name(self):
        sku = self.sku.get_name
        sha = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return "-".join([sku, sha])
    
