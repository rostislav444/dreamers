from django.db.models import Prefetch
from rest_framework import serializers

from apps.material.models import ProductPartMaterials
from apps.material.serializers.serializers_materials_set import ProductPartSerializer
from apps.product.models import Product, Camera
from apps.product.serializers import ProductPartSceneSerializer


class CatalogueCameraSerializer(serializers.ModelSerializer):
    parts = ProductPartSceneSerializer(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = ['parts']


class CatalogueProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_class.name')
    sku = serializers.SerializerMethodField()
    part_images = serializers.SerializerMethodField()
    material_parts = serializers.SerializerMethodField()
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
    def get_material_parts(obj):
        if not obj.product_class.materials_set:
            return []

        qs = obj.product_class.materials_set.parts.all().prefetch_related(
            Prefetch(
                'material_groups__materials',
                queryset=ProductPartMaterials.objects.filter(preferred=True)
            )
        )
        return ProductPartSerializer(qs, many=True, read_only=True).data

    @staticmethod
    def get_camera(obj):
        model_3d = obj.model_3d.first()
        if model_3d:
            camera = model_3d.cameras.filter(rad_z=90).prefetch_related('parts__materials').first()
            if camera:
                return CatalogueCameraSerializer(camera).data
