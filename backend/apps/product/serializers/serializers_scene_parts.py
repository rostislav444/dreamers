from rest_framework import serializers

from apps.product.models import Product3DBlenderModel, CameraLocations, ProductPartScene, ProductPartSceneMaterial


class ProductPartSceneMaterialSerializer(serializers.Serializer):
    material = serializers.CharField(source='material.id')

    class Meta:
        model = ProductPartSceneMaterial
        fields = ['material']


class ProductPartSceneSerializer(serializers.Serializer):
    part = serializers.CharField(source='part.blender_name')
    materials = ProductPartSceneMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPartScene
        fields = '__all__'


# class CameraLocationsSerializer(serializers.Serializer):
#     parts = ProductPartSceneSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = CameraLocations
#         fields = '__all__'


# class Product3DModelSerializer(serializers.Serializer):
#     cameras = CameraLocationsSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Product3DBlenderModel
#         fields = '__all__'
#
#     def get_part_scene(self, obj):
#         data = {}
#
#         materials_set = obj.product_class.materials_set
#         for part in materials_set.parts.all():
#             data[part.id] = {}
#             for material_group in part.material_groups.all():
#                 data[part.id][material_group.id] = {}
#
#         return data


__all__ = [
    'ProductPartSceneMaterialSerializer',
    'ProductPartSceneSerializer'
]