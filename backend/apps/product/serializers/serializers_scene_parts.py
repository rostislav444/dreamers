from rest_framework import serializers

from apps.material.serializers import ProductPartSerializerLite
from apps.product.models import ProductPartScene, ProductPartSceneMaterial, ProductPartSceneMaterialImage


class ProductPartSceneMaterialImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPartSceneMaterialImage
        fields = ['scene_material', 'image']


class ProductPartSceneMaterialSerializer(serializers.ModelSerializer):
    material = serializers.CharField(source='material.id')
    image = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()

    class Meta:
        model = ProductPartSceneMaterial
        fields = ['id', 'material', 'image', 'thumbnails']

    def get_image(self, obj):
        if hasattr(obj, 'image'):
            return obj.image.image.name

    def get_thumbnails(self, obj):
        if hasattr(obj, 'image'):
            return obj.image.image_thumbnails




class ProductPartSceneSerializer(serializers.ModelSerializer):
    part = ProductPartSerializerLite()
    materials = serializers.SerializerMethodField()

    class Meta:
        model = ProductPartScene
        fields = ['part', 'materials']

    def get_materials(self, obj):
        only_new = False
        request = self.context.get('request')
        if request:
            only_new = request.GET.get('only_new')

        # qs = obj.materials.filter(image__isnull=True) if only_new else obj.materials.all()
        qs = obj.materials.all()

        return ProductPartSceneMaterialSerializer(qs, many=True, read_only=True).data


__all__ = [
    'ProductPartSceneMaterialSerializer',
    'ProductPartSceneSerializer'
]
