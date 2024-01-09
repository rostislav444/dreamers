from itertools import product


def generate_sku(instance):
    from apps.product.models import ProductPartMaterials, Sku, SkuMaterials

    data = {}

    for part in instance.parts.all():
        data[part] = tuple(ProductPartMaterials.objects.filter(
            group__product_part=part).distinct())

    keys = data.keys()
    combinations = [tuple(zip(keys, values)) for values in product(*data.values())]

    for variant in instance.products.all():
        variant.sku.all().delete()
        for combination in combinations:
            code = '__'.join([variant.code, *[material[1].code for material in combination]])

            sku = Sku(product=variant, code=code)
            sku.save()

            for material in combination:
                sku_material = SkuMaterials(sku=sku, material=material[1])
                sku_material.save()
