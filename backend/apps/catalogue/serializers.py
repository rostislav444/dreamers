from rest_framework import serializers

from apps.product.models import Product
from apps.product.serializers import CatalogueSkuSerializer
from apps.material.serializers.serializers_materials_set import CatalogueProductPartSerializer


class CatalogueProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_class.name')
    parts = serializers.SerializerMethodField()
    sku = serializers.SerializerMethodField()
    part_images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'price', 'parts', 'sku', 'part_images']

    def get_part_images(self, obj):
        return obj.get_parts_images

    @staticmethod
    def get_parts(obj):
        if not obj.product_class.materials_set:
            return

        parts = CatalogueProductPartSerializer(obj.product_class.materials_set.parts, many=True).data
        materials_ids = [material['id'] for part in parts for material in part['materials']]
        return {
            'sku': CatalogueSkuSerializer(
                obj.sku.filter(images__isnull=False, materials__material__id__in=materials_ids).distinct(), many=True
            ).data,
            'parts': parts
        }

    @staticmethod
    def get_sku(obj):
        return []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        data = self.get_parts(instance)
        representation.update(data)
        return representation
