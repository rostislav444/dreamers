from django.db.models import signals
from django.dispatch import receiver

from apps.product.models import ProductClass, Product, SkuImages, ProductCustomizedPart
from apps.product.utils import generate_sku


@receiver(signals.post_save, sender=ProductClass)
def generate_sku_from_options(sender, instance, **kwargs):
    if instance.pk and instance.generate_sku_from_options:
        generate_sku(instance)
        ProductClass.objects.filter(pk=instance.pk).update(generate_sku_from_options=False)

# @receiver(signals.post_save, sender=ProductPartMaterialsGroups)
# def add_plette_to_material_group_colors(sender, instance, **kwargs):
#     if instance.pk and instance.add_palette:
#         for palette_color in instance.add_palette.colors.all():
#             material, _ = ProductPartMaterials.objects.get_or_create(group=instance, color=palette_color.color)
#
#         ProductPartMaterialsGroups.objects.filter(pk=instance.pk).update(add_palette=None)


@receiver(signals.post_save, sender=Product)
def delete_all_sku_images(sender, instance, **kwargs):
    if instance.pk and instance.remove_images:
        SkuImages.objects.filter(sku__product=instance).delete()
        Product.objects.filter(pk=instance.pk).update(remove_images=False)

    if instance.pk and instance.product_class.materials_set:
        for part in instance.product_class.materials_set.parts.all():
            obj, _ = ProductCustomizedPart.objects.get_or_create(part=part, product=instance)

