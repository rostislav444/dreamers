from rest_framework import serializers

from apps.product.models import Product
from apps.product.serializers import CatalogueSkuSerializer
from apps.product.serializers.serializers_materials import CatalogueProductPartSerializer


class CatalogueProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_class.name')
    parts = CatalogueProductPartSerializer(source='product_class.parts', many=True)
    sku = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'price', 'parts', 'sku']

    @staticmethod
    def get_sku(obj):
        return CatalogueSkuSerializer(obj.sku.filter(images__isnull=False).distinct()[:12], many=True).data
