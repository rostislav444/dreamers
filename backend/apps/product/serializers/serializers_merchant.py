from rest_framework import serializers

from apps.product.models import Sku, Product
from apps.category.models import Category


class GoogleMerchantSkuSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='code')
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    image_link = serializers.SerializerMethodField()
    additional_image_link = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    gtin = serializers.SerializerMethodField()
    mpn = serializers.SerializerMethodField()
    condition = serializers.CharField(default='new')
    google_product_category = serializers.SerializerMethodField()
    product_type = serializers.SerializerMethodField()
    material = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = Sku
        fields = [
            'id', 'title', 'description', 'link', 'image_link', 'additional_image_link',
            'availability', 'price', 'brand', 'gtin', 'mpn', 'condition',
            'google_product_category', 'product_type', 'material', 'color', 'size'
        ]

    def get_title(self, obj):
        return f"{obj.product.product_class.name} {obj.code}"

    def get_description(self, obj):
        return obj.product.product_class.description or ""

    def get_link(self, obj):
        # Замените на реальный URL вашего сайта
        base_url = "https://dreamers.com.ua"
        return f"{base_url}/product/{obj.product.product_class.slug}/{obj.product.pk}/{obj.pk}/"

    def get_image_link(self, obj):
        if obj.images.exists():
            # Берем первое изображение
            image = obj.images.first()
            return image.image.url
        return ""

    def get_additional_image_link(self, obj):
        additional_images = []
        # Берем все изображения кроме первого
        for image in obj.images.all()[1:]:
            additional_images.append(image.image.url)
        return additional_images

    def get_availability(self, obj):
        # Проверяем наличие товара
        if obj.quantity > 0:
            return "in stock"
        return "out of stock"

    def get_price(self, obj):
        # Получаем цену из продукта или устанавливаем значение по умолчанию
        price = obj.product.price or 0
        # Валюта может быть разной в зависимости от вашего магазина
        return f"{price} RUB"

    def get_brand(self, obj):
        # Здесь можно указать бренд вашего магазина
        return "Dreamers"

    def get_gtin(self, obj):
        # Global Trade Item Number (если есть)
        return ""

    def get_mpn(self, obj):
        # Manufacturer Part Number (если есть)
        return obj.code

    def get_google_product_category(self, obj):
        # Здесь нужно указать категорию Google Merchant
        # Пример: "Мебель > Мебель для гостиной > Диваны"
        category_path = []
        category = obj.product.product_class.category
        
        # Собираем путь категорий
        while category:
            category_path.insert(0, category.name)
            try:
                category = category.parent
            except:
                category = None
                
        return " > ".join(category_path)

    def get_product_type(self, obj):
        # Тип продукта в вашем магазине
        return obj.product.product_class.category.name

    def get_material(self, obj):
        # Получаем материалы
        materials = []
        for material in obj.materials.all():
            materials.append(str(material))
        return ", ".join(materials)

    def get_color(self, obj):
        # Получаем цвета из материалов (если применимо)
        colors = []
        for material in obj.materials.all():
            if hasattr(material, 'material') and hasattr(material.material, 'color'):
                colors.append(material.material.color.name)
        return ", ".join(set(colors))

    def get_size(self, obj):
        # Получаем размеры из продукта
        width = obj.product.width
        height = obj.product.height
        depth = obj.product.depth
        
        if width and height and depth:
            return f"{width}x{height}x{depth} мм"
        return "" 