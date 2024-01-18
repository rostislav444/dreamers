from rest_framework import serializers

from apps.material.serializers import ColorSerializer
from apps.product.models import Product3DBlenderModel, ProductClass, ProductPart, ProductPartMaterialsGroups, \
    ProductPartMaterials, Product, Sku


class SkuRenderSerializer(serializers.ModelSerializer):
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Sku
        fields = ['id', 'materials']

    @staticmethod
    def get_materials(obj):
        return {material.material.group.product_part.blender_name: material.material.id for material in
                obj.materials.all()}


class ProductRender3DBlenderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product3DBlenderModel
        fields = ['obj', 'mtl']


class ProductRenderSerializer(serializers.ModelSerializer):
    sku = serializers.SerializerMethodField()
    model_3d = ProductRender3DBlenderModelSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'code', 'model_3d', 'sku', ]

    @staticmethod
    def get_sku(obj):
        qs = obj.sku.filter(images__isnull=True).distict()
        return SkuRenderSerializer(qs, many=True, read_only=True).data




class ProductPartRenderMaterialSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    material = serializers.SerializerMethodField()

    class Meta:
        model = ProductPartMaterials
        fields = ('id', 'color', 'material',)

    def get_material(self, obj):
        if obj.material and obj.material.blender_material:
            data = obj.material.blender_material.get_data
            data['name'] = obj.material.blender_material.name
            return data
        return None


class ProductPartRenderMaterialsGroupsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='group.type')
    materials = ProductPartRenderMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPartMaterialsGroups
        fields = ('product_part', 'type', 'materials',)


class ProductPartRenderSerializer(serializers.ModelSerializer):
    material_groups = ProductPartRenderMaterialsGroupsSerializer(many=True, read_only=True)

    class Meta:
        model = ProductPart
        fields = ('blender_name', 'name', 'material_groups')


class ProductRenderWithSkuSerializer(serializers.ModelSerializer):
    parts = ProductPartRenderSerializer(many=True, read_only=True)
    products = ProductRenderSerializer(many=True, read_only=True)

    class Meta:
        model = ProductClass
        fields = ['id', 'parts', 'products']
