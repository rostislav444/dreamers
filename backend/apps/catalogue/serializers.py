from rest_framework import serializers

from apps.product.models import Product
from apps.product.serializers import CatalogueSkuSerializer, CameraLocationsSerializer
from apps.material.serializers.serializers_materials_set import CatalogueProductPartSerializer, ProductPartSerializer, \
    ProductPartSerializerLite, MaterialSetSerializer


class CatalogueProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_class.name')
    sku = serializers.SerializerMethodField()
    part_images = serializers.SerializerMethodField()
    material_parts = ProductPartSerializer(source='product_class.materials_set.parts', many=True, read_only=True)
    camera = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'price', 'material_parts', 'sku', 'part_images', 'camera']

    def get_part_images(self, obj):
        return obj.get_parts_images

    @staticmethod
    def get_sku(obj):
        return []

    @staticmethod
    def get_camera(obj):
        if obj.model_3d:
            camera = obj.model_3d.cameras.filter(rad_z=90).first()
            if camera:
                return CameraLocationsSerializer(camera).data
