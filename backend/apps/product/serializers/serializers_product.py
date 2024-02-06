from rest_framework import serializers

from apps.product.models import Product
from apps.material.serializers import ProductPartSerializer
from .serializers_sku import SkuSerializer
from ...category.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_class.name')
    description = serializers.CharField(source='product_class.description')
    sku = SkuSerializer(read_only=True, many=True)
    parts = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'code', 'sku', 'parts', 'categories', 'width', 'height', 'depth']

    @staticmethod
    def get_parts(obj):
        materials_set = obj.product_class.materials_set
        if materials_set:
            return ProductPartSerializer(materials_set.parts, many=True).data


    @staticmethod
    def get_categories(obj):
        return [CategorySerializer(category).data for category in obj.product_class.category.get_ancestors(include_self=True)]
