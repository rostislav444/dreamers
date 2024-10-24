from io import BytesIO

from PIL import Image
from django.core.files import File
from django.db.models import signals
from django.dispatch import receiver

from apps.abstract.fields import FileNaming
from apps.material.models import BlenderMaterial, Material, RecommendedCombinations, RecommendedCombinationsParts


def crop_and_save_image(blender_material, material):
    storage = material.image.storage

    ext = blender_material.col.name.split('.')[-1]

    with blender_material.col.open() as f:
        original_image = Image.open(f)

        x, y = 0, 0
        w, h = 120, 120

        image_file = BytesIO()
        # Обрезаем изображение
        cropped_image = original_image.crop((x, y, x + w, y + h))
        if ext == 'png':
            cropped_image = cropped_image.convert('RGB')
        cropped_image.save(image_file, format='JPEG', quality=100)
        image_file.seek(0)

        # Сохраняем в хранилище
        naming = FileNaming()
        naming.name = 'image'
        image_name = naming.generate_filename(material, '.jpeg')
        storage.save(image_name, File(image_file))

        Material.objects.filter(pk=material.pk).update(image=image_name)


def calculate_aspect_ratio(instance: BlenderMaterial):
    aspect_ratio = 1

    with instance.col.open() as f:
        image = Image.open(f)
        width, height = image.size
        if height != 0:
            aspect_ratio = round(width / height, 2)

    BlenderMaterial.objects.filter(pk=instance.pk).update(aspect_ratio=aspect_ratio)


@receiver(signals.post_save, sender=BlenderMaterial)
def get_blender_material_image(sender, instance, **kwargs):
    if instance.col:
        calculate_aspect_ratio(instance)
        # if hasattr(instance, 'material'):
        #     crop_and_save_image(instance, instance)


@receiver(signals.post_save, sender=Material)
def get_material_image(sender, instance, **kwargs):
    if instance.blender_material:
        crop_and_save_image(instance.blender_material, instance)



@receiver(signals.post_save, sender=RecommendedCombinations)
def generate_combinations_parts_groups(sender, instance, **kwargs):
    for part in instance.material_set.parts.all():
        RecommendedCombinationsParts.objects.get_or_create(combination=instance, part=part)