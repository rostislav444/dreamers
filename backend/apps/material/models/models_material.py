from PIL import Image
from django.db import models

from apps.abstract.fields import DeletableFileField, DeletableImageField
from apps.abstract.models import NameSlug
import copy


class MaterialGroups(models.Model):
    TYPES = (
        ('material', 'material',),
        ('color', 'color',),
    )
    PRICE_LEVEL_CHOICES = (
        ('group', 'Цена на группу'),
        ('sub_group', 'Цена на суб группу'),
        ('material', 'Цена на материал'),
    )

    type = models.CharField(max_length=25, choices=TYPES, default=TYPES[0][0])
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Цена, м2', blank=True)
    price_level = models.CharField(choices=PRICE_LEVEL_CHOICES, max_length=9, null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Группа материалов'
        verbose_name_plural = '2. Группы материалов'

    def __str__(self):
        return '{} ({})'.format(self.name, self.type)


class MaterialSubGroup(models.Model):
    group = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Цена, м2', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Суб группа материалов'
        verbose_name_plural = '3. Суб группы материалов'


class BlenderMaterial(NameSlug):
    copy_from = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    preview = DeletableImageField(null=True, blank=True, verbose_name='Preview')

    col = DeletableFileField(null=True, blank=True, verbose_name='Color')
    color = models.ForeignKey('Color', on_delete=models.CASCADE, null=True, blank=True)
    nrm_gl = DeletableFileField(null=True, blank=True, verbose_name='Norma GL')
    nrm_dx = DeletableFileField(null=True, blank=True, verbose_name='Norma DX')
    bump = DeletableFileField(null=True, blank=True, verbose_name='Bump')
    bump16 = DeletableFileField(null=True, blank=True, verbose_name='Bump 16 bit')
    disp = DeletableFileField(null=True, blank=True, verbose_name='Displacement')
    disp16 = DeletableFileField(null=True, blank=True, verbose_name='Displacement 16 bit')
    rgh = DeletableFileField(null=True, blank=True, verbose_name='Roughness')
    mtl = DeletableFileField(null=True, blank=True, verbose_name='Metalness')
    refl = DeletableFileField(null=True, blank=True, verbose_name='Reflection')
    ao = DeletableFileField(null=True, blank=True, verbose_name='Ambient Occlusion')

    rgh_num = models.DecimalField(max_digits=5, decimal_places=2, default=0.5, verbose_name='Roughness Value',
                                  blank=True)
    mtl_num = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name='Metalness Value',
                                  blank=True)
    refl_num = models.DecimalField(max_digits=5, decimal_places=2, default=0.5, verbose_name='Reflection Value',
                                   blank=True)
    ao_num = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, verbose_name='AO Value', blank=True)

    scale = models.DecimalField(max_digits=5, decimal_places=2, default=1, verbose_name='Scale', blank=True)
    aspect_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=1, verbose_name='Aspect Ratio',
                                       blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.copy_from and not self.pk:
            original = self.copy_from
            for field in original._meta.fields:
                if field.name not in ['id', 'pk', 'copy_from']:
                    setattr(self, field.name, getattr(original, field.name))
            self.copy_from = None

        if not self.col and not self.color:
            raise ValueError('You must provide either a col or a color')

        if self.color:
            color_name = self.color.name
            if color_name not in self.name:
                self.name = f'{self.name} ({color_name})'
        super().save(*args, **kwargs)

    @property
    def get_data(self):
        data = {}
        for field in self._meta.fields:
            if isinstance(field, DeletableFileField) and getattr(self, field.name).name:
                data[field.name] = getattr(self, field.name).name
        return data

    class Meta:
        verbose_name = 'Материал Blender'
        verbose_name_plural = '5. Материалы Blender'


class Material(NameSlug):
    group = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE, related_name='materials')
    sub_group = models.ForeignKey(MaterialSubGroup, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='materials')

    image = DeletableImageField(null=True, blank=True)
    blender_material = models.OneToOneField(BlenderMaterial, null=True, blank=True, on_delete=models.PROTECT,
                                            related_name='material')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Цена, м2', blank=True)

    def __str__(self):
        return ' / '.join([self.group.name, self.name])

    class Meta:
        ordering = ('group', 'sub_group', 'name')
        verbose_name = 'Материал'
        verbose_name_plural = '4. Материалы'


__all__ = [
    'MaterialGroups',
    'MaterialSubGroup',
    'BlenderMaterial',
    'Material'
]
