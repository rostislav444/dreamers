from rest_framework import serializers

from apps.material.serializers import ColorSerializer
from apps.product.models import ProductPart, ProductPartMaterialsGroups, ProductPartMaterials


class ProductPartMaterialSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    material = serializers.SerializerMethodField()

    class Meta:
        model = ProductPartMaterials
        fields = ('color', 'material',)

    def get_material(self, obj):
        if obj.material and obj.material.blender_material:
            data = obj.material.blender_material.get_data
            data['name'] = obj.material.blender_material.name
            return data
        return None


class ProductPartMaterialsGroupsSerializer(serializers.ModelSerializer):
    product_part = serializers.CharField(source='product_part.name')
    type = serializers.CharField(source='group.type')
    materials = ProductPartMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPartMaterialsGroups
        fields = ('product_part', 'type', 'materials',)


class ProductPartSerializer(serializers.ModelSerializer):
    material_groups = ProductPartMaterialsGroupsSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPart
        fields = ('blender_name', 'name', 'material_groups')
