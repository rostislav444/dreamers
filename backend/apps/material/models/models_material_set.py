from django.core.exceptions import ValidationError
from django.db import models
from slugify import slugify
from unidecode import unidecode

from apps.abstract.models import NameSlug
from apps.material.models import Material, MaterialGroups, MaterialSubGroup, Color, Palette


class MaterialsSet(NameSlug):
    class Meta:
        verbose_name = 'Набор материалов'
        verbose_name_plural = '1. Наборы материалов'


class ProductStaticPart(models.Model):
    materials_set = models.ForeignKey(MaterialsSet, on_delete=models.CASCADE, related_name='static_parts')
    name = models.CharField(max_length=255)
    blender_name = models.CharField(max_length=255)
    group = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='product_class_static_materials',
                                 null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='product_class_static_color',
                              null=True, blank=True)

    def __str__(self):
        return self.name


class ProductPart(models.Model):
    materials_set = models.ForeignKey(MaterialsSet, on_delete=models.CASCADE, related_name='parts')
    name = models.CharField(max_length=255)
    blender_name = models.CharField(max_length=255)

    def __str__(self):
        return '%s (3d name: %s)' % (self.name, self.blender_name)


class ProductPartMaterialsGroups(models.Model):
    product_part = models.ForeignKey(ProductPart, on_delete=models.CASCADE, related_name='material_groups')
    group = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE, related_name='product_class_groups')
    add_palette = models.ForeignKey(Palette, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{} / {} ({}: {})'.format(
            self.product_part.name,
            self.group.name,
            self.group.type + 's',
            self.materials.count()
        )


class ProductPartMaterialsSubGroups(models.Model):
    product_part = models.ForeignKey(ProductPart, on_delete=models.CASCADE, related_name='material_sub_groups')
    group = models.ForeignKey(ProductPartMaterialsGroups, on_delete=models.CASCADE, related_name='sub_groups')
    sub_group = models.ForeignKey(MaterialSubGroup, on_delete=models.CASCADE,
                                  related_name='product_class_sub_groups')


# class ProductPartMaterialsManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().select_related('group__group')


class ProductPartMaterials(models.Model):
    group = models.ForeignKey(ProductPartMaterialsGroups, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='product_class_materials', null=True,
                                 blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='product_parts', null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, editable=False)
    preferred = models.BooleanField(default=False)

    # objects = ProductPartMaterialsManager()

    class Meta:
        ordering = ['color__ral', 'material']

    def __str__(self):
        value = self.get_value
        return ' / '.join([self.group.product_part.name, value])

    @property
    def group_type(self):
        return self.group.group.type

    @property
    def get_value(self):
        return str(self.material) if self.group_type == 'material' else str(self.color)

    @property
    def get_code(self):
        names = [slugify(unidecode(name)) for name in
                 [self.group.product_part.blender_name, self.group_type, self.get_value]]
        return '_'.join(names)

    def clean(self):
        if not any([self.material, self.color]):
            if self.group_type == 'material':
                raise ValidationError({'material': 'Choose one'})
            else:
                raise ValidationError({'color': 'Choose one'})

    def save(self, *args, **kwargs):
        self.code = self.get_code
        super(ProductPartMaterials, self).save()


class RecommendedCombinations(NameSlug):
    material_set = models.ForeignKey(MaterialsSet, on_delete=models.CASCADE, related_name='recommended_combinations')

    class Meta:
        verbose_name = 'Рекомендованная комбинация'
        verbose_name_plural = '2. Рекомендованные комбинации'

    @property
    def get_name(self):
        if self.pk and self.parts.exists():
            return '-'.join([part.get_name for part in self.parts.all()])
        return '-'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.get_name
        super(RecommendedCombinations, self).save()


class RecommendedCombinationsParts(models.Model):
    combination = models.ForeignKey(RecommendedCombinations, on_delete=models.CASCADE, related_name='parts')
    part = models.ForeignKey(ProductPart, on_delete=models.CASCADE, related_name='recommended_combinations')
    material = models.ForeignKey(ProductPartMaterials, on_delete=models.CASCADE,
                                 related_name='recommended_combinations_part', null=True, blank=True)

    class Meta:
        ordering = ('combination', 'part', 'material')

    def __str__(self):
        if hasattr(self, 'part') and hasattr(self, 'material'):
            return '{} / {}'.format(self.part, self.material or '-')
        return '-'

    @property
    def get_name(self):
        return '%s %s' % (unidecode(self.part.name), self.material.get_value if hasattr(self, 'material') and getattr(self, 'material') else '-')

    # def save(self):
    #     name = '-'.join([part.get_name for part in  self.combination.parts.all()])
    #     RecommendedCombinationsParts.objects.filter(pk=self.pk).update(name=name)
    #     super(RecommendedCombinationsParts, self).save()


__all__ = [
    'MaterialsSet',
    'ProductStaticPart',
    'ProductPart',
    'ProductPartMaterialsGroups',
    'ProductPartMaterialsSubGroups',
    'ProductPartMaterials',
    'RecommendedCombinations',
    'RecommendedCombinationsParts'
]
