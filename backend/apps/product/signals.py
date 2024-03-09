from django.core.exceptions import ObjectDoesNotExist
from django.db.models import signals
from django.dispatch import receiver

from apps.product.models import ProductClass, Product, SkuImages, ProductCustomizedPart, Product3DBlenderModel, \
    CameraLocations, ProductPartScene, ProductPartSceneMaterial
from .tasks import task_generate_product_class_sku, task_generate_product_sku


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
                pos_x=product.height / 1000 * 2.4,
                pos_y=0,
                pos_z=product.height / 1000 / 2,
                rad_x=90,
                rad_y=0,
                rad_z=90
            )
            direct_location.save()


# @receiver(signals.post_save, sender=CameraLocations)
# def create_scene_product_part_materials(sender, instance, **kwargs):
#     if instance.pk:
#         product = instance.model_3d.product
#         materials_set = product.product_class.material_set
#         if materials_set:
#             for part in materials_set.parts.all():
#                 product_part_scene, _ = ProductPartScene.objects.get_or_create(camera=instance, part=part)
#                 for material_group in part.material_groups.all():
#                     for material in material_group.materials.all():
#                         ProductPartSceneMaterial.objects.get_or_create(part=product_part_scene, material=material)


@receiver(signals.post_save, sender=CameraLocations)
def create_scene_product_part_materials(sender, instance, **kwargs):
    def create_product_part_scenes(materials_set):
        for part in materials_set.parts.all():
            product_part_scene, _ = get_or_create_product_part_scene(instance, part)
            create_product_part_scene_materials(product_part_scene, part)

    def get_or_create_product_part_scene(camera, part):
        return ProductPartScene.objects.get_or_create(camera=camera, part=part)

    def create_product_part_scene_materials(product_part_scene, part):
        for material_group in part.material_groups.all():
            for material in material_group.materials.all():
                ProductPartSceneMaterial.objects.get_or_create(part=product_part_scene, material=material)

    if instance.pk:
        product = instance.model_3d.product
        materials_set = product.product_class.materials_set
        if materials_set:
            create_product_part_scenes(materials_set)
