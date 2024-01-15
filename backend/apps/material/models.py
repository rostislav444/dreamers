import PIL
from PIL import ImageColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
from colormath.color_objects import sRGBColor, LabColor
from django.db import models

from apps.abstract.fields import DeletableFileField, DeletableImageField
from apps.abstract.models import NameSlug

import numpy

def patch_asscalar(a):
    return a.item()

setattr(numpy, "asscalar", patch_asscalar)


class BaseColor(NameSlug):
    hex = models.CharField(max_length=7)
    rgb = models.JSONField(default=list, blank=True)
    lvl = models.PositiveIntegerField(default=0)
    index = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s - %d' % (self.name, self.lvl)

    class Meta:
        ordering = ['index', 'lvl']

    def save(self, *args, **kwargs):
        self.rgb = PIL.ImageColor.getrgb(self.hex)
        super(BaseColor, self).save(*args, **kwargs)


class Palette(NameSlug):
    pass


def calculate_cie76_distance(color1, color2):
    """
    Вычисляет расстояние между двумя цветами в модели CIELAB (CIE76).
    """
    color1_lab = convert_color(sRGBColor(*color1, is_upscaled=True), LabColor)
    color2_lab = convert_color(sRGBColor(*color2, is_upscaled=True), LabColor)

    # Use item() to convert the result to a Python scalar
    distance = delta_e_cie1976(color1_lab, color2_lab)
    return distance


def find_closest_color_cie76(target_color, color_list):
    """
    Находит ближайший цвет из списка цветов к заданному целевому цвету в модели CIELAB (CIE76).
    """
    closest_color = min(color_list, key=lambda color: calculate_cie76_distance(target_color, color))
    return closest_color


class Color(NameSlug):
    mid_color = models.ForeignKey(BaseColor, on_delete=models.CASCADE, null=True, blank=True)
    ral = models.CharField(max_length=24, null=True, blank=True)
    hex = models.CharField(max_length=7)
    rgb = models.JSONField(default=list, blank=True)
    lvl = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ral']

    def __str__(self):
        if self.ral:
            return ' '.join([self.name, self.ral])
        return self.name

    def closest_color(self, rgb):
        colors = BaseColor.objects.all()
        rgb_colors = colors.values_list('rgb', flat=True)

        # r, g, b = rgb
        # color_diffs = []
        # for color in rgb_colors:
        #     cr, cg, cb = color
        #     color_diff = sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        #     color_diffs.append((color_diff, color))
        # closest = min(color_diffs)[1]

        closest = find_closest_color_cie76(rgb, rgb_colors)

        return colors.filter(rgb=closest).first()

    def save(self, *args, **kwargs):
        self.rgb = PIL.ImageColor.getrgb(self.hex)
        self.mid_color = self.closest_color(self.rgb)
        super(Color, self).save(*args, **kwargs)


class PaletteColor(models.Model):
    palette = models.ForeignKey(Palette, on_delete=models.CASCADE, related_name='colors')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='palettes')

    class Meta:
        unique_together = (('palette', 'color'),)


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

    def __str__(self):
        return '{} ({})'.format(self.name, self.type)


class MaterialSubGroup(models.Model):
    group = models.ForeignKey(MaterialGroups, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Цена, м2', blank=True)

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

    image = DeletableImageField(null=True, blank=True)
    blender_material = models.OneToOneField(BlenderMaterial, null=True, blank=True, on_delete=models.PROTECT,
                                            related_name='material')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Цена, м2', blank=True)

    def __str__(self):
        return ' / '.join([self.group.name, self.name])
