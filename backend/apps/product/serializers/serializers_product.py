from rest_framework import serializers

from apps.product.models import Product
from .serializers_materials import ProductPartSerializer
from .serializers_sku import SkuSerializer
from ...category.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_class.name')
    sku = SkuSerializer(read_only=True, many=True)
    parts = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'code', 'sku', 'parts', 'categories']

    @staticmethod
    def get_parts(obj):
        return ProductPartSerializer(obj.product_class.parts.all(), many=True).data


    @staticmethod
    def get_categories(obj):
        return [CategorySerializer(category).data for category in obj.product_class.category.get_ancestors(include_self=True)]
