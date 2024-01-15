import json

from django.core.management.base import BaseCommand

from apps.material.models import Palette, BaseColor


def generate_shades(base_color):
    shades = []

    n = 4
    k = 1 / n / 2
    for i in range(1, n + 1):
        new_color = [int(tone * (1 - i / n + k)) for tone in base_color]

        shades.append(new_color)

    return shades


def lighten_color(base_color):
    def lighten_color(rgb, factor=0.2):
        r, g, b = rgb
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        return (r, g, b)

    shades = []

    for n in [2, 4, 6, 8]:
        shades.append(lighten_color(base_color, n / 10))

    return shades


def rgb_to_hex(rgb):
    r, g, b = rgb
    _hex = '#%02x%02x%02x' % (r, g, b)
    return _hex


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = 'data/main_colors.json'

        BaseColor.objects.all().delete()

        white, _ = BaseColor.objects.get_or_create(name='White', hex='#ffffff', lvl=0, index=0)
        black, _ = BaseColor.objects.get_or_create(name='Black', hex='#000000', lvl=8, index=13)

        base_num = 4

        with open(file_path, 'r') as json_file:
            reader = json.load(json_file)

            for index, color in enumerate(reader['colors'], 1):
                main_color, _ = BaseColor.objects.get_or_create(name=color['name'], hex=color['hex'], index=index, lvl=base_num)

                for n, shade in enumerate(generate_shades(main_color.rgb)):
                    _color, _ = BaseColor.objects.get_or_create(
                        name=color['name'],
                        hex=rgb_to_hex(shade),
                        index=index,
                        lvl=base_num + n + 1
                    )

                for n, shade in enumerate(lighten_color(main_color.rgb)):
                    _color, _ = BaseColor.objects.get_or_create(
                        name=color['name'],
                        hex=rgb_to_hex(shade),
                        index=index,
                        lvl=base_num - n - 1
                    )


