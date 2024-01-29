from collections import OrderedDict

from rest_framework import serializers

from apps.material.serializers import ColorSerializer, MaterialSerializer, ColorLiteSerializer
from apps.product.models import ProductPart, ProductPartMaterialsGroups, ProductPartMaterials, \
    ProductPartMaterialsSubGroups


class ProductPartMaterialSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    sub_group = serializers.SerializerMethodField()

    class Meta:
        model = ProductPartMaterials
        fields = ('id', 'color', 'material', 'sub_group',)

    @staticmethod
    def get_sub_group(obj):
        if obj.material and obj.material.sub_group:
            return obj.material.sub_group.id
        return None


class ProductPartMaterialsSubGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPartMaterialsSubGroups
        fields = ('id', 'name')


class ProductPartMaterialsGroupsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='group.type')
    name = serializers.CharField(source='group.name')
    materials = serializers.SerializerMethodField()
    sub_groups = ProductPartMaterialsSubGroupsSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPartMaterialsGroups
        fields = ('id', 'type', 'name', 'sub_groups', 'materials',)

    @staticmethod
    def get_materials(obj):
        materials_qs = obj.materials.filter(
            sku_materials__sku__product__product_class=obj.product_part.product_class
        ).distinct()
        return ProductPartMaterialSerializer(materials_qs, many=True, read_only=True).data


class ProductPartSerializer(serializers.ModelSerializer):
    material_groups = ProductPartMaterialsGroupsSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPart
        fields = ('id', 'name', 'material_groups')


''' Catalogue '''


class CatalogueProductPartMaterialSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()
    color = ColorLiteSerializer()

    class Meta:
        model = ProductPartMaterials
        fields = ['id', 'material', 'color']

    def to_representation(self, instance):
        result = super(CatalogueProductPartMaterialSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


class CatalogueProductPartMaterialsGroupsSerializer(serializers.ModelSerializer):
    materials = CatalogueProductPartMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPartMaterialsGroups
        fields = ['id', 'materials']


class CatalogueProductPartSerializer(serializers.ModelSerializer):
    materials = serializers.SerializerMethodField()

    class Meta:
        model = ProductPart
        fields = ['id', 'name', 'materials']

    @staticmethod
    def get_materials(obj):
        materials = ProductPartMaterials.objects.filter(
            group__product_part=obj,
            sku_materials__sku__product__product_class=obj.product_class
        ).distinct()[:8]
        return CatalogueProductPartMaterialSerializer(materials, many=True).data
