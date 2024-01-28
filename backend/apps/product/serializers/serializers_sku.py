from rest_framework import serializers

from apps.product.models import Sku, SkuMaterials, SkuImages
from apps.product.serializers.serializers_materials import ProductPartMaterialSerializer


class SkuMaterialsSerializer(serializers.ModelSerializer):
    material = ProductPartMaterialSerializer()
    part_name = serializers.CharField(source='get_material_part_name')

    class Meta:
        model = SkuMaterials
        fields = ['id', 'material', 'part_name']


class SkuImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkuImages
        fields = ['sku', 'image', 'index']


class SkuSerializer(serializers.ModelSerializer):
    images = SkuImagesSerializer(many=True, read_only=True)
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Sku
        fields = ['id', 'code', 'images', 'materials']

    @staticmethod
    def get_images(obj):
        return [image.image_thumbnails['s'] for image in obj.images.all()]

    @staticmethod
    def get_materials(obj):
        return {material.material.group.product_part.id: material.material.id for material in obj.materials.all()}


class CatalogueSkuSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Sku
        fields = ['id', 'code', 'images', 'materials']

    @staticmethod
    def get_images(obj):
        return [
            image.image_thumbnails['m']
            for image in obj.images.all()
        ]

    @staticmethod
    def get_materials(obj):
        return {material.material.group.product_part.id: material.material.id for material in obj.materials.all()}

