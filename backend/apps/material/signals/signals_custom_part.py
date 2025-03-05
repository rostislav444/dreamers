from apps.product.models import ProductCustomizedPart, ProductCustomizedPartMaterialGroup
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=ProductCustomizedPart)
def create_product_customized_part(sender, instance, created, **kwargs):
    if instance.part:
        for material_group in instance.part.material_groups.all():
            item, _ = ProductCustomizedPartMaterialGroup.objects.get_or_create(
                parent=instance,
                material_group=material_group.group
            )

            item.save()