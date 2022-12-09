
from math import sqrt
from PIL import ImageColor


def get_closet_color(color_hex, color_rgb, colors):
    if not color_hex and not color_rgb:
        return None

    colors_rgb = colors.values_list('rgb', flat=True)

    r, g, b = ImageColor.getrgb(color_hex) if color_hex else color_rgb
    color_diffs = []
    for color in colors_rgb:
        cr, cg, cb = color
        color_diff = sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        color_diffs.append((color_diff, color))

    print(color_diffs)

    closest = min(color_diffs)[1]
    return colors.filter(rgb=closest).first()

