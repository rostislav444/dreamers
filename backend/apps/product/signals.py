from io import BytesIO

from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db.models import signals
import math

from django.dispatch import receiver

from apps.product.models import ProductClass, Product, SkuImages, ProductCustomizedPart, Product3DBlenderModel, \
    Camera, ProductPartScene, ProductPartSceneMaterial, CameraInteriorLayer, \
    CameraInteriorLayerMaterial, CameraInteriorLayerMaterialGroup, Sku
from .tasks import task_generate_product_class_sku
from ..material.models import RecommendedCombinations


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

        if instance.generate_sku_from_materials:
            for combination in RecommendedCombinations.objects.filter(material_set=instance.product_class.materials_set):
                sku, _ = Sku.objects.get_or_create(
                    product=instance,
                    code=str(combination),
                )
                materials = [getattr(part, 'material') for part in combination.parts.all()]
                if materials:
                    sku.materials.set(materials)

                sku.save()
            Product.objects.filter(pk=instance.pk).update(generate_sku_from_materials=False)


def calculate_camera_position(radius, angle_degrees):
    # Преобразование угла из градусов в радианы
    angle_radians = math.radians(angle_degrees)

    # Расчет координат камеры
    x = radius * math.sin(angle_radians)
    y = radius * math.cos(angle_radians)

    return x, y


def calculate_camera_radius(width_m, height_m, depth_m, fov_degrees, aspect_width=3, aspect_height=2):
    # Convert the field of view angle from degrees to radians (horizontal FOV)
    fov_horizontal_radians = math.radians(fov_degrees)

    # Calculate the vertical field of view based on the aspect ratio
    fov_vertical_radians = 2 * math.atan(math.tan(fov_horizontal_radians / 2) * (aspect_height / aspect_width))

    # Calculate the radius based on the width (assuming the object's width is the limiting dimension)
    radius_width = width_m / (2 * math.tan(fov_horizontal_radians / 2))

    # Calculate the radius based on the height (assuming the object's height is the limiting dimension)
    radius_height = height_m / (2 * math.tan(fov_vertical_radians / 2))

    # Use the maximum of the two radii to ensure the object fits within the camera view
    radius = max(radius_width, radius_height)

    return radius


def get_camera_level(height_m, radius, render_from_eye_level, eye_level):
    rad_x = 90
    middle_pos = height_m / 2

    if render_from_eye_level:
        delta_height = eye_level - middle_pos
        tilt_angle_degrees = math.degrees(math.atan(delta_height / radius))
        rad_x -= tilt_angle_degrees
        return rad_x, eye_level
    else:
        return rad_x, middle_pos


def get_rotation_coordinates(product: Product, instance: Product3DBlenderModel):
    result = []

    start_angle, step = 30, 30
    fov_degrees, steps, eye_level, render_from_eye_level = (instance.fov_degrees, instance.steps, instance.eye_level,
                                                            instance.render_from_eye_level)

    width_m, height_m, depth_m = product.width / 1000, product.height / 1000, product.depth / 1000
    radius = calculate_camera_radius(width_m, height_m, depth_m, fov_degrees)

    rad_x, camera_level = get_camera_level(height_m, radius, eye_level, render_from_eye_level)

    for i in range(steps):
        angle = 90 if range == 1 else start_angle + i * step
        x, y = calculate_camera_position(radius, angle)

        rad_z = -angle + 180

        result.append({
            'location': (x, y, camera_level),
            'angle': (rad_x, 0, rad_z)
        })
    return result


@receiver(signals.post_save, sender=Product3DBlenderModel)
def generate_camera_locations(sender, instance, **kwargs):
    if instance.pk:
        coordinates = get_rotation_coordinates(instance.product, instance)
        # coordinates = get_rotation_coordinates(9, radius=product.height / 1000 * 3.2, z=product.height / 1000 / 2)

        for i, coordinate in enumerate(coordinates):
            location = coordinate['location']
            angle = coordinate['angle']

            try:
                Camera.objects.get(model_3d=instance, rad_z=angle[2])
            except ObjectDoesNotExist:
                direct_location = Camera(
                    model_3d=instance,
                    pos_x=location[0],
                    pos_y=location[1],
                    pos_z=location[2],
                    rad_x=angle[0],
                    rad_y=angle[1],
                    rad_z=angle[2]
                )
                direct_location.save()


# @receiver(signals.post_save, sender=Camera)
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


def create_interior_layer_materials(camera):
    if camera.pk:
        interior = camera.model_3d.product.product_class.interior
        if interior:
            for interior_layer in interior.layers.all():
                camera_interior_layer, _ = CameraInteriorLayer.objects.get_or_create(
                    camera=camera, interior_layer=interior_layer)
                for material_group in interior_layer.material_groups.all():
                    camera_interior_layer_material_group, _ = CameraInteriorLayerMaterialGroup.objects.get_or_create(
                        layer=camera_interior_layer, material_group=material_group)
                    for material in material_group.materials.all():
                        camera_interior_layer_material, _ = CameraInteriorLayerMaterial.objects.get_or_create(
                            group=camera_interior_layer_material_group, material=material)


@receiver(signals.post_save, sender=Camera)
def camera_location_post_save(sender, instance, **kwargs):
    create_scene_product_part_materials(instance)
    create_interior_layer_materials(instance)


@receiver(signals.post_save, sender=Product3DBlenderModel)
def model_3d_post_save(sender, instance, **kwargs):
    for camera in instance.cameras.all():
        create_scene_product_part_materials(camera)
        create_interior_layer_materials(camera)


def merge_images(images):
    opened_images = [Image.open(image) for image in images]

    # Берем размеры первого изображения для базы
    base_image = opened_images[0].copy()

    # Накладываем остальные изображения одно за другим на базовое
    for img in opened_images[1:]:
        base_image.paste(img, (0, 0), img)  # Если изображения имеют прозрачность, передаем img как маску

    return base_image


def add_white_background(image):
    # Создаем белый фон с размерами исходного изображения
    white_bg = Image.new("RGB", image.size, (255, 255, 255))

    # Если у изображения есть альфа-канал, накладываем его на белый фон
    if image.mode in ('RGBA', 'LA'):
        white_bg.paste(image, (0, 0), image)  # Используем прозрачность как маску
    else:
        white_bg.paste(image, (0, 0))  # Если прозрачности нет, просто накладываем

    return white_bg

@receiver(signals.post_save, sender=Sku)
def generate_sku_images(sender, instance, **kwargs):
    if instance.pk and instance.generate_images:
        for model_3d in instance.product.model_3d.all():
            for camera in model_3d.cameras.all():
                images = []
                for camera_part in camera.parts.all():
                    sku_material = instance.materials.get(group__product_part=camera_part.part)
                    try:
                        material = camera_part.materials.get(material=sku_material)
                    except ObjectDoesNotExist:
                        continue
                    images.append(material.image.image.file)
                if not images:
                    continue

                merged_image = merge_images(images)

                # Сохраняем изображение в буфер памяти
                buffer = BytesIO()
                merged_image_with_bg = add_white_background(merged_image)
                merged_image = merged_image_with_bg.convert("RGB")
                merged_image.save(buffer, format='JPEG', quality=100)
                buffer.seek(0)

                # Создаем объект SkuImages и передаем буфер как изображение
                sku_image, _ = SkuImages.objects.get_or_create(sku=instance, camera=camera)
                sku_image.image.save(f'sku_{instance.pk}_camera_{camera.pk}.jpeg', ContentFile(buffer.read()), save=False)
                sku_image.save()

        # Обновляем флаг generate_images
        Sku.objects.filter(pk=instance.pk).update(generate_images=False)
