import abc

from django.db import models

from apps.material.models import Material, MaterialGroups, Color, Palette


class PartAbstract(models.Model):
    name = models.CharField(max_length=255)
    blender_name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ProductStaticPartAbstract(PartAbstract):
    group = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='product_class_static_materials',
                                 null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='product_class_static_color',
                              null=True, blank=True)

    class Meta:
        abstract = True


class ProductPartAbstract(PartAbstract):
    area = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Площадь, м2')

    class Meta:
        abstract = True


class ProductPartMaterialsGroupsAbstract(models.Model):
    group = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE)
    add_palette = models.ForeignKey(Palette, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True

    @property
    @abc.abstractmethod
    def product_part(self):
        pass

    def __str__(self):
        return '{} / {} ({}: {})'.format(
            self.product_part.name,
            self.group.name,
            self.group.type + 's',
            self.materials.count()
        )
