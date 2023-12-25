import PIL
from PIL import ImageColor
from django.db import models

from apps.abstract.fields import DeletableFileField
from apps.abstract.models import NameSlug


class MidColor(NameSlug):
    hex = models.CharField(max_length=7)


class Color(NameSlug):
    mid_color = models.ForeignKey(MidColor, on_delete=models.CASCADE, null=True, blank=True)
    ral = models.CharField(max_length=9, null=True, blank=True)
    hex = models.CharField(max_length=7)
    rgb = models.JSONField(default=list)

    class Meta:
        ordering = ['mid_color', 'ral', 'hex']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        print('self.hex', self.hex)
        self.rgb = PIL.ImageColor.getrgb(self.hex)
        super(Color, self).save(*args, **kwargs)


class MaterialGroups(models.Model):
    TYPES = (
        ('material', 'material',),
        ('color', 'color',),
    )
    type = models.CharField(max_length=25, choices=TYPES, default=TYPES[0][0])
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return '{} ({})'.format(self.name, self.type)


class MaterialSubGroup(models.Model):
    group = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BlenderMaterial(NameSlug):
    col = DeletableFileField(verbose_name='Color')
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

    def __str__(self):
        return self.name

    @property
    def get_data(self):
        data = {}
        for field in self._meta.fields:
            if isinstance(field, DeletableFileField) and getattr(self, field.name).name:
                data[field.name] = getattr(self, field.name).name
        return data



class Material(NameSlug):
    group = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE, related_name='materials')
    sub_group = models.ForeignKey(MaterialSubGroup, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='materials')

    image = DeletableFileField(null=True, blank=True)
    blender_material = models.OneToOneField(BlenderMaterial, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        names = [self.group.name, self.name]
        if self.sub_group:
            names.insert(1, self.sub_group.name)
        return ' / '.join(names)
