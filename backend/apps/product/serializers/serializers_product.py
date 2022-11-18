from rest_framework import serializers

from apps.product.models import Product, ProductAttribute, Product3DBlenderModel, ProductOptionPriceMultiplier
from .serializers_sku import SkuSerializer


class ProductOptionPriceMultiplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionPriceMultiplier
        fields = ['value', 'option_group']


class Product3DBlenderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product3DBlenderModel
        fields = ['blend', 'blend1', 'mtl', 'obj']


class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'attribute']


class ProductSerializer(serializers.ModelSerializer):
    model_3d = Product3DBlenderModelSerializer(read_only=True)
    sku = SkuSerializer(read_only=True, many=True)
    attributes = ProductAttributesSerializer(read_only=True, many=True)
    multipliers = ProductOptionPriceMultiplierSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'price', 'model_3d', 'sku', 'attributes', 'multipliers']


