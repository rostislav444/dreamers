import unidecode
from django.utils.text import slugify


def generate_variants_from_dimensions(obj):
    from apps.product.models import Product

    initial_price = obj.initial_price
    initial_square_decimeter_price = initial_price / (obj.min_width * obj.min_height * obj.min_depth)

    data_lists = {
        'width': [obj.min_width],
        'height': [obj.min_height],
        'depth': [obj.min_depth]
    }

    for key in data_lists.keys():
        min_key, max_key, step_key = 'min_' + key, 'max_' + key, key + '_step'
        if getattr(obj, max_key) and getattr(obj, step_key):
            range_value = int((getattr(obj, max_key) - getattr(obj, min_key)) / getattr(obj, step_key))
            data_lists[key] += [getattr(obj, min_key) + (i + 1) * getattr(obj, step_key) for i in range(range_value)]

    create = []
    update = []

    products = Product.objects.filter(product_class=obj)

    for width in data_lists['width']:
        for height in data_lists['height']:
            for depth in data_lists['depth']:
                exists = products.filter(width=width, height=height, depth=depth).first()
                slug = unidecode.unidecode(obj.name)
                code = slugify(slug) + '_w' + str(width) + '_h' + str(height) + '_d' + str(depth)

                price = int(width * height * depth * initial_square_decimeter_price / 10) * 10

                print(price)

                if exists:
                    exists.code = code
                    exists.price = price
                    update.append(exists)
                else:
                    product = Product(
                        product_class=obj,
                        code=code,
                        price=price,
                        width=width,
                        height=height,
                        depth=depth
                    )
                    create.append(product)

    # Сначала создаём новые объекты
    created = Product.objects.bulk_create(create)
    created_ids = [p.id for p in created]

    # Обновляем существующие объекты
    Product.objects.bulk_update(update, ['code', 'price'])
    updated_ids = [p.id for p in update]

    products.exclude(id__in=created_ids+updated_ids).delete()



