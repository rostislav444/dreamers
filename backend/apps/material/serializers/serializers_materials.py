from rest_framework import serializers

from apps.material.models import Color, Material, BlenderMaterial


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'hex', 'ral', 'rgb')


class ColorLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'hex')


class BlenderMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlenderMaterial
        fields = '__all__'


class Material3DSerializer(serializers.ModelSerializer):
    blender_material = BlenderMaterialSerializer(read_only=True)

    class Meta:
        model = Material
        fields = ('id', 'name', 'image', 'blender_material')


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'image',)


__all__ = [
    'ColorSerializer',
    'ColorLiteSerializer',
    'MaterialSerializer',
    'Material3DSerializer'
]
