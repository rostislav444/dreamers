from itertools import product


def get_combinations(materials_set):
    from apps.material.models import ProductPartMaterials

    data = {}

    for part in materials_set.parts.all():
        data[part] = tuple(ProductPartMaterials.objects.filter(
            group__product_part=part).distinct())
    keys = data.keys()
    return [tuple(zip(keys, values)) for values in product(*data.values())]


def generate_sku_material_combinations(variant, combinations):
    from apps.product.models import Sku, SkuMaterials

    ids = []

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
        print(code)
        ids.append(sku.id)

        for material in combination:
            sku_material = SkuMaterials(sku=sku, material=material[1])
            sku_material.save()
    Sku.objects_no_distinct.filter(product=variant).exclude(id__in=ids).delete()


def generate_product_class_sku(product_class_id):
    from apps.product.models import ProductClass

    instance = ProductClass.objects.get(pk=product_class_id)
    if not instance.materials_set:
        return
    combinations = get_combinations(instance.materials_set)
    for variant in instance.products.all():
        generate_sku_material_combinations(variant, combinations)


def generate_product_sku(product_id):
    from apps.product.models import Product

    instance = Product.objects.get(pk=product_id)
    if not instance.product_class.materials_set:
        return
    combinations = get_combinations(instance.materials_set)
    generate_sku_material_combinations(instance, combinations)
