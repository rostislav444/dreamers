import uuid
from io import BytesIO

from PIL import Image
from django.core.files import File
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.abstract.fields import FileNaming
from apps.material.models import BlenderMaterial, RecommendedCombinations, RecommendedCombinationsParts, \
    ProductPartMaterials, MaterialsSet, ProductStaticPart, ProductPart, ProductPartMaterialsGroups, \
    ProductPartMaterialsSubGroups


def crop_and_save_image(blender_material, material):
    storage = material.preview.storage

    ext = blender_material.col.name.split('.')[-1]

    with blender_material.col.open() as f:
        # print(f_open)
        original_image = Image.open(f)

        x, y = 0, 0
        w, h = 240, 240

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
        print(image_name)
        storage.save(image_name, File(image_file))

        BlenderMaterial.objects.filter(pk=blender_material.pk).update(preview=image_name)


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
        crop_and_save_image(instance, instance)


@receiver(signals.post_save, sender=RecommendedCombinations)
def generate_combinations_parts_groups(sender, instance, created, **kwargs):
    # Пропускаем автоматическое создание частей при копировании набора материалов
    if created and not hasattr(instance, '_copying'):
        for part in instance.material_set.parts.all():
            RecommendedCombinationsParts.objects.get_or_create(combination=instance, part=part)


@receiver(post_save, sender=MaterialsSet)
def copy_materials_set(sender, instance, created, **kwargs):
    if created and instance.copy_from is not None:
        # Copy ProductStaticPart
        for static_part in instance.copy_from.static_parts.all():
            ProductStaticPart.objects.create(
                materials_set=instance,
                name=static_part.name,
                blender_name=static_part.blender_name,
                group=static_part.group,
                material=static_part.material,
                color=static_part.color
            )

        # Copy ProductPart and related
        for product_part in instance.copy_from.parts.all():
            # Create new ProductPart
            new_part = ProductPart.objects.create(
                materials_set=instance,
                name=product_part.name,
                blender_name=product_part.blender_name
            )

            # Copy ProductPartMaterialsGroups and related
            for material_group in product_part.material_groups.all():
                new_material_group = ProductPartMaterialsGroups.objects.create(
                    product_part=new_part,
                    group=material_group.group,
                    add_palette=material_group.add_palette
                )

                # Copy ProductPartMaterialsSubGroups
                for sub_group in material_group.sub_groups.all():
                    ProductPartMaterialsSubGroups.objects.create(
                        product_part=new_part,
                        group=new_material_group,
                        sub_group=sub_group.sub_group
                    )

                # Copy ProductPartMaterials
                for material in material_group.materials.all():
                    ProductPartMaterials.objects.create(
                        group=new_material_group,
                        material=material.material,
                        color=material.color,
                        preferred=material.preferred
                    )

        # Copy RecommendedCombinations and related
        for combination in instance.copy_from.recommended_combinations.all():
            new_combination = RecommendedCombinations.objects.create(
                material_set=instance,
                name=combination.name,
                _copying=True  # Маркер для пропуска автоматического создания частей
            )

            # Find corresponding new parts for recommendations
            for combo_part in combination.parts.all():
                if combo_part.material:  # Копируем только части с материалами
                    new_part = instance.parts.get(name=combo_part.part.name)

                    # Find corresponding new material if exists
                    new_material = None
                    for material_group in new_part.material_groups.all():
                        try:
                            new_material = material_group.materials.get(
                                material=combo_part.material.material,
                                color=combo_part.material.color
                            )
                            break
                        except ProductPartMaterials.DoesNotExist:
                            continue

                    if new_material:
                        RecommendedCombinationsParts.objects.create(
                            combination=new_combination,
                            part=new_part,
                            material=new_material
                        )

            # Удаляем временный маркер
            delattr(new_combination, '_copying')
            new_combination.save()

        # Clear copy_from after successful copy
        MaterialsSet.objects.filter(pk=instance.pk).update(copy_from=None)


