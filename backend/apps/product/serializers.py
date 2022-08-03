from rest_framework import serializers
from apps.product.models import Product, ProductImage




class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'image'
        ]




class ProductSerializer(serializers.ModelSerializer):
    name =        serializers.CharField(source='product_class.name', max_length=255)
    slug =        serializers.CharField(source='product_class.slug', max_length=255)
    description = serializers.CharField(source='product_class.description')
    images =      ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name', 
            'slug', 
            'description', 
            'price', 
            'slug', 
            'images'
        ]

