from django.db.models import signals
from django.dispatch import receiver

from apps.product.models import ProductClass, ProductPartMaterialsGroups, ProductPartMaterials
from apps.product.utils import generate_sku


@receiver(signals.post_save, sender=ProductClass)
def generate_sku_from_options(sender, instance, **kwargs):
    if instance.pk and instance.generate_sku_from_options:
        generate_sku(instance)
        ProductClass.objects.filter(pk=instance.pk).update(generate_sku_from_options=False)


@receiver(signals.post_save, sender=ProductPartMaterialsGroups)
def add_plette_to_material_group_colors(sender, instance, **kwargs):
    if instance.pk and instance.add_palette:
        for palette_color in instance.add_palette.colors.all():
            material, _ = ProductPartMaterials.objects.get_or_create(group=instance, color=palette_color.color)

        ProductPartMaterialsGroups.objects.filter(pk=instance.pk).update(add_palette=None)
