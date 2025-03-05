from rest_framework import serializers

from apps.product.models import ProductCustomizedPart, ProductCustomizedPartMaterialGroup

__all__ = ['ProductCustomizedPartMaterialGroupSerializer', 'ProductCustomizedPartSerializer']


class ProductCustomizedPartMaterialGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCustomizedPartMaterialGroup
        fields = ['group_price', 'price']


class ProductCustomizedPartSerializer(serializers.ModelSerializer):
    material_groups = serializers.SerializerMethodField()
    part = serializers.CharField(source='part.blender_name', read_only=True)

    class Meta:
        model = ProductCustomizedPart
        fields = ['material_groups', 'part', 'area']

    @staticmethod
    def get_material_groups(obj):
        return {
            group.material_group.name: ProductCustomizedPartMaterialGroupSerializer(group).data
            for group in obj.material_groups.all()
        }
