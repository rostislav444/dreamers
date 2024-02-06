import PIL
import numpy
from PIL import ImageColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
from colormath.color_objects import sRGBColor, LabColor
from django.db import models

from apps.abstract.models import NameSlug


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


def srgb_to_linearrgb(c):
    if c < 0:
        return 0
    elif c < 0.04045:
        return c / 12.92
    else:
        return ((c + 0.055) / 1.055) ** 2.4


def hex_to_rgb(hex_color, alpha=1):
    hex_value = int(hex_color.lstrip('#'), 16)
    r = (hex_value & 0xff0000) >> 16
    g = (hex_value & 0x00ff00) >> 8
    b = hex_value & 0x0000ff
    return tuple([srgb_to_linearrgb(c / 0xff) for c in (r, g, b)] + [alpha])


def hex_to_real_rgb(hex_color):
    (r, g, b) = ImageColor.getcolor(hex_color, "RGB")
    return [r, g, b]


class Color(NameSlug):
    mid_color = models.ForeignKey(BaseColor, on_delete=models.CASCADE, null=True, blank=True)
    ral = models.CharField(max_length=24, null=True, blank=True)
    hex = models.CharField(max_length=7)
    rgb_real = models.JSONField(default=list, blank=True)
    rgb = models.JSONField(default=list, blank=True)
    lvl = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['mid_color__lvl', 'mid_color__index']

    def __str__(self):
        if self.ral:
            return ' '.join([self.name, self.ral])
        return self.name

    def closest_color(self, rgb):
        colors = BaseColor.objects.all()
        rgb_colors = colors.values_list('rgb', flat=True)
        closest = find_closest_color_cie76(rgb, rgb_colors)
        return colors.filter(rgb=closest).first()

    def save(self, *args, **kwargs):
        [r, g, b, _] = hex_to_rgb(self.hex)
        self.rgb = [r, g, b]

        self.rgb_real = hex_to_real_rgb(self.hex)
        self.mid_color = self.closest_color(self.rgb_real)
        super(Color, self).save(*args, **kwargs)


class PaletteColor(models.Model):
    palette = models.ForeignKey(Palette, on_delete=models.CASCADE, related_name='colors')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='palettes')

    class Meta:
        unique_together = (('palette', 'color'),)


__all__ = [
    'BaseColor',
    'Palette',
    'Color',
    'PaletteColor'
]
