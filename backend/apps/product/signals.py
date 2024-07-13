from django.core.exceptions import ObjectDoesNotExist
from django.db.models import signals
import math
import mathutils

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


def get_rotation_coordinates(steps=24, radius=4, z=2):
    result = []

    startAngle = 30

    if steps > 360:
        steps = 360
    step = 180 / steps

    for i in range(steps):
        angle = startAngle + i * step
        x = radius * math.sin(math.radians(angle))
        y = radius * math.cos(math.radians(angle))

        rotation = math.pi
        if angle > 0:
            rotation -= math.pi * 2 * angle / 360

        # Convert rotation angle from radians to degrees
        rad_x = int(math.degrees(math.pi * 0.40))
        rad_z = int(math.degrees(rotation))

        result.append({
            'location': (x, y, z),
            'angle': (90, 0, rad_z)
        })
    return result


@receiver(signals.post_save, sender=Product3DBlenderModel)
def generate_camera_locations(sender, instance, **kwargs):
    if instance.pk:
        product = instance.product
        coordinates = get_rotation_coordinates(9, radius=product.height / 1000 * 3.2, z=product.height / 1000 / 2)

        for i, coordinate in enumerate(coordinates):
            location = coordinate['location']
            angle = coordinate['angle']

            try:
                CameraLocations.objects.get(model_3d=instance, rad_z=angle[2])
            except ObjectDoesNotExist:
                direct_location = CameraLocations(
                    model_3d=instance,
                    pos_x=location[0],
                    pos_y=location[1],
                    pos_z=location[2],
                    rad_x=angle[0],
                    rad_y=angle[1],
                    rad_z=angle[2]
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


def create_scene_product_part_materials(camera_instance):
    def get_or_create_product_part_scene(camera, part):
        return ProductPartScene.objects.get_or_create(camera=camera, part=part)

    def create_product_part_scene_materials(product_part_scene, part):
        for material_group in part.material_groups.all():
            for material in material_group.materials.all():
                ProductPartSceneMaterial.objects.get_or_create(part=product_part_scene, material=material)

    def create_product_part_scenes(materials_set):
        for part in materials_set.parts.all():
            product_part_scene, _ = get_or_create_product_part_scene(camera_instance, part)
            create_product_part_scene_materials(product_part_scene, part)

    if camera_instance.pk:
        product = camera_instance.model_3d.product
        materials_set = product.product_class.materials_set
        if materials_set:
            create_product_part_scenes(materials_set)


@receiver(signals.post_save, sender=CameraLocations)
def camera_location_post_save(sender, instance, **kwargs):
    create_scene_product_part_materials(instance)


@receiver(signals.post_save, sender=Product3DBlenderModel)
def model_3d_post_save(sender, instance, **kwargs):
    for camera in instance.cameras.all():
        create_scene_product_part_materials(camera)
