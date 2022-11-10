from rest_framework import serializers
from apps.product.models import Product
from apps.product.serializers import SkuSerializer, ProductClassOptionGroupSerializer
from collections import OrderedDict


class CatalogueProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_class.name', max_length=255)
    slug = serializers.CharField(source='product_class.slug', max_length=255)
    description = serializers.CharField(source='product_class.description')
    sku = SkuSerializer(read_only=True, many=True)
    options_groups = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'slug', 'images', 'sku', 'options_groups']

    @staticmethod
    def get_options_groups(obj):
        data = OrderedDict()
        for group in obj.product_class.option_groups.filter(image_dependency=True):
            data[group.slug] = ProductClassOptionGroupSerializer(group).data
        return data
