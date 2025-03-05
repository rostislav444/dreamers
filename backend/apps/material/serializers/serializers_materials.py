from rest_framework import serializers

from apps.abstract.fields import DeletableFileField
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
    color = ColorSerializer(read_only=True)

    class Meta:
        model = BlenderMaterial
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)

        # Process all fields that are DeletableFileField and add their URL to the representation
        data.update(self.get_file_fields_representation(instance, request))

        return data

    def get_file_fields_representation(self, instance, request):
        file_fields_data = {}
        # Find all fields of the model that are DeletableFileField
        for field in instance._meta.fields:
            if isinstance(field, DeletableFileField):
                file_field = getattr(instance, field.name)
                if file_field and hasattr(file_field, 'url'):
                    # Forming an absolute or relative URL for each file field
                    file_fields_data[field.name] = request.build_absolute_uri(
                        file_field.url) if request else file_field.url

        return file_fields_data


class Material3DSerializer(serializers.ModelSerializer):
    blender_material = BlenderMaterialSerializer(read_only=True)

    class Meta:
        model = Material
        fields = ('id', 'name', 'image', 'blender_material')


class MaterialSerializer(serializers.ModelSerializer):
    color = ColorLiteSerializer(read_only=True)
    class Meta:
        model = Material
        fields = ('id', 'name', 'image', 'color')


__all__ = [
    'ColorSerializer',
    'ColorLiteSerializer',
    'MaterialSerializer',
    'Material3DSerializer'
]
