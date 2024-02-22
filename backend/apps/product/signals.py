from django.core.exceptions import ObjectDoesNotExist
from django.db.models import signals
from django.dispatch import receiver
from .tasks import task_generate_product_class_sku, task_generate_product_sku

from apps.product.models import ProductClass, Product, SkuImages, ProductCustomizedPart, Product3DBlenderModel, \
    CameraLocations


@receiver(signals.post_save, sender=ProductClass)
def generate_sku_from_options(sender, instance, **kwargs):
    if instance.pk and instance.generate_sku_from_options:
        task_generate_product_class_sku.delay(instance.pk)
        ProductClass.objects.filter(pk=instance.pk).update(generate_sku_from_options=False)


@receiver(signals.post_save, sender=Product)
def delete_all_sku_images(sender, instance, **kwargs):
    if instance.pk:
        if instance.remove_images:
            SkuImages.objects.filter(sku__product=instance).delete()
            Product.objects.filter(pk=instance.pk).update(remove_images=False)

        if instance.product_class.materials_set:
            for part in instance.product_class.materials_set.parts.all():
                obj, _ = ProductCustomizedPart.objects.get_or_create(part=part, product=instance)

        if instance.generate_sku:
            task_generate_product_sku.delay(instance.pk)
            Product.objects.filter(pk=instance.pk).update(generate_sku=False)






@receiver(signals.post_save, sender=Product3DBlenderModel)
def generate_camera_locations(sender, instance, **kwargs):
    if instance.pk:
        try:
            CameraLocations.objects.get(model_3d=instance, rad_x=90)
        except ObjectDoesNotExist:
            product = instance.product

            direct_location = CameraLocations(
                model_3d=instance,
                pos_x=product.height / 1000 * 2.44,
                pos_y=0,
                pos_z=product.height / 1000 / 2,
                rad_x=90,
                rad_y=0,
                rad_z=90
            )
            direct_location.save()
