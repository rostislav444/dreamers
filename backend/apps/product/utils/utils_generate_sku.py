from itertools import product
from django.db.models import Q

def generate_sku(instance):
    from apps.product.models import Sku, SkuMaterials
    from apps.material.models import ProductPartMaterials

    data = {}

    if not instance.materials_set:
        return

    for part in instance.materials_set.parts.all():
        data[part] = tuple(ProductPartMaterials.objects.filter(
            group__product_part=part).distinct())

    keys = data.keys()
    combinations = [tuple(zip(keys, values)) for values in product(*data.values())]

    ids = []

    for variant in instance.products.all():
        print(variant, variant)
        for combination in combinations:

            filtered_sku = Sku.objects.filter(product=variant)
            for material in combination:
                filtered_sku = filtered_sku.filter(materials__material=material[1])

            sku = filtered_sku.first()

            if sku:
                ids.append(sku.id)
                continue

            code = '__'.join([variant.code, *[material[1].code for material in combination]])

            sku = Sku(product=variant, code=code)
            sku.save()
            ids.append(sku.id)

            for material in combination:
                sku_material = SkuMaterials(sku=sku, material=material[1])
                sku_material.save()

        Sku.objects_no_distinct.filter(product=variant).exclude(id__in=ids).delete()

