import json

from django.core.management.base import BaseCommand

from apps.material.models import Palette, Color, PaletteColor


def rgb_to_hex(rgb):
    r, g, b = rgb
    _hex = '#%02x%02x%02x' % (r, g, b)
    return _hex


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = 'data/ral_2025.json'

        palette, _ = Palette.objects.get_or_create(name='RAL 2025+')

        with open(file_path, 'r') as json_file:
            reader = json.load(json_file)

            for clr in reader:
                color, _ = Color.objects.get_or_create(
                    name=clr['name'],
                    hex=clr['hex'],
                    ral=clr['ral'],
                )
                color.save()

                PaletteColor.objects.get_or_create(color=color, palette=palette)