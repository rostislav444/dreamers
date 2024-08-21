from django.db import models

from apps.abstract.models import NameSlug
from apps.material.models import ProductPartMaterialsGroups, Material, Color, MaterialGroups


class Interior(NameSlug):
    class Meta:
        verbose_name = 'Интерьер'
        verbose_name_plural = '1. Интерьеры'


class InteriorLayer(NameSlug):
    interior = models.ForeignKey(Interior, on_delete=models.CASCADE, related_name='layers')

    class Meta:
        verbose_name = 'Слой интерьера'
        verbose_name_plural = '2. Слои интерьера'


class InteriorLayerMaterialGroup(models.Model):
    layer = models.ForeignKey(InteriorLayer, on_delete=models.CASCADE, related_name='material_groups')
    material_group = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE, related_name='interior_layers_groups')

    class Meta:
        verbose_name = 'Группа материалов интерьера'
        verbose_name_plural = '3. Группы материалов интерьера'

    def __str__(self):
        return str(self.material_group)


class InteriorMaterial(models.Model):
    group = models.ForeignKey(InteriorLayerMaterialGroup, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Материал слоя'
        verbose_name_plural = '4. Материалы слоя'

    @property
    def group_type(self):
        return self.group.material_group.type

    @property
    def get_value(self):
        return str(self.material) if self.group_type == 'material' else str(self.color)

    def __str__(self):
        return self.get_value
