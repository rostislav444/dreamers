from collections import OrderedDict

from rest_framework import serializers

from apps.material.serializers.serializers_materials import ColorSerializer, MaterialSerializer, ColorLiteSerializer
from apps.material.models import ProductPart, ProductPartMaterialsGroups, ProductPartMaterials, \
    ProductPartMaterialsSubGroups, MaterialsSet


class ProductPartMaterialSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    sub_group = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = ProductPartMaterials
        fields = ('id', 'color', 'material', 'sub_group',)

    @staticmethod
    def get_name(obj):
        if obj.color:
            return obj.color.name
        return obj.material.name

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
    materials = ProductPartMaterialSerializer(many=True, read_only=True)
    sub_groups = ProductPartMaterialsSubGroupsSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPartMaterialsGroups
        fields = ('id', 'type', 'name', 'sub_groups', 'materials',)


class ProductPartSerializerLite(serializers.ModelSerializer):
    class Meta:
        model = ProductPart
        fields = ('id', 'name', 'blender_name',)


class ProductPartSerializer(ProductPartSerializerLite):
    material_groups = ProductPartMaterialsGroupsSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPart
        fields = ('id', 'name', 'blender_name', 'material_groups',)


class MaterialSetSerializer(serializers.ModelSerializer):
    parts = ProductPartSerializer(many=True, read_only=True)

    class Meta:
        model = MaterialsSet
        fields = ['id', 'name', 'slug', 'parts']


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
            sku_materials__sku__product__product_class__materials_set=obj.materials_set
        ).distinct()[:8]

        return CatalogueProductPartMaterialSerializer(materials, many=True).data




