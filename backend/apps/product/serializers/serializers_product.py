from rest_framework import serializers

from apps.product.models import Product, ProductAttribute, Product3DBlenderModel
from apps.attribute.serializers import ProductAttributeGroupSerializer, ProductAttributeSerializer
from .serializers_sku import SkuSerializer


class Product3DBlenderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product3DBlenderModel
        fields = ['blend', 'blend1', 'mtl', 'obj']


class ProductAttributesSerializer(serializers.ModelSerializer):
    attribute_group = ProductAttributeGroupSerializer(read_only=True)
    attribute = ProductAttributeSerializer(source='value_attribute', read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ['attribute_group', 'attribute']

    def get_attribute(self, instance):
        return instance.value_attribute.value


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_class.name', max_length=255)
    slug = serializers.CharField(source='product_class.slug', max_length=255)
    description = serializers.CharField(source='product_class.description')
    model_3d = Product3DBlenderModelSerializer(read_only=True)
    sku = SkuSerializer(read_only=True, many=True)
    attributes = ProductAttributesSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'price',
            'name',
            'slug',
            'description',
            'model_3d',
            'sku',
            'attributes'
        ]


