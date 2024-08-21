from rest_framework import serializers
from apps.interior.models import Interior, InteriorMaterial
from apps.material.serializers import ColorSerializer, Material3DSerializer


class InteriorMaterialSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    material = Material3DSerializer(read_only=True)

    class Meta:
        model = InteriorMaterial
        fields = ['id', 'material', 'color']


class InteriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interior
