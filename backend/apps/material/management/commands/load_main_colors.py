import json

from django.core.management.base import BaseCommand

from apps.material.models import Palette, Color


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

        Color.objects.all().delete()

        palette, _ = Palette.objects.get_or_create(name='Main colors')

        with open(file_path, 'r') as json_file:
            reader = json.load(json_file)

            for color in reader['colors']:
                main_color, _ = Color.objects.get_or_create(name=color['name'], hex=color['hex'], lvl=5)

                for n, shade in enumerate(generate_shades(main_color.rgb)):
                    _color, _ = Color.objects.get_or_create(
                        name=color['name'],
                        hex=rgb_to_hex(shade),
                        lvl=5 + n + 1
                    )

                for n, shade in enumerate(lighten_color(main_color.rgb)):
                    _color, _ = Color.objects.get_or_create(
                        name=color['name'],
                        hex=rgb_to_hex(shade),
                        lvl=5 - n - 1
                    )
