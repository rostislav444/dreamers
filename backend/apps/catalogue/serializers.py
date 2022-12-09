from rest_framework import serializers
from collections import OrderedDict
from apps.product.models import ProductClass, Product, Sku, SkuImages, SkuOptions
from apps.product.serializers import SkuSerializer, ProductClassOptionGroupSerializer


class CatalogueSkuOptionsSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    option_id = serializers.IntegerField(source='option.id')

    class Meta:
        model = SkuOptions
        fields = ['id', 'option_id', 'value']

    def get_value(self, obj):
        return obj.option.value


class CatalogueSkuImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkuImages
        fields = ['image']


class CatalogueSkuSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    images = CatalogueSkuImagesSerializer(read_only=True, many=True)

    class Meta:
        model = Sku
        fields = ['id', 'options', 'images']

    def get_options(self, obj):
        data = []
        for option in obj.options.all():
            data.append([option.option.attribute_group.slug, option.option.id])
        return OrderedDict(data)


class CatalogueProductSerializer(serializers.ModelSerializer):
    sku = CatalogueSkuSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'price', 'slug', 'images', 'sku']


class CatalogueProductClassSerializer(serializers.ModelSerializer):
    products = CatalogueProductSerializer(read_only=True, many=True)
    option_groups = ProductClassOptionGroupSerializer(read_only=True, many=True)

    class Meta:
        model = ProductClass
        fields = ['id', 'name', 'slug', 'description', 'products', 'option_groups']
