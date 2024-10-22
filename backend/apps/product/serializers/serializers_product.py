from rest_framework import serializers

from apps.material.serializers import ProductPartSerializer
from apps.product.models import Product
from .serializers_render import ProductRender3DBlenderModelSerializer
from .serializers_sku import SkuSerializer
from ...category.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_class.name')
    description = serializers.CharField(source='product_class.description')
    material_parts = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    model_3d = ProductRender3DBlenderModelSerializer(read_only=True, many=True)

    # sku = SkuSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'code', 'material_parts', 'categories', 'width', 'height',
                  'depth', 'model_3d']

    @staticmethod
    def get_material_parts(obj):
        materials_set = obj.product_class.materials_set
        if materials_set:
            return ProductPartSerializer(materials_set.parts, many=True).data

    @staticmethod
    def get_categories(obj):
        return [CategorySerializer(category).data for category in
                obj.product_class.category.get_ancestors(include_self=True)]



