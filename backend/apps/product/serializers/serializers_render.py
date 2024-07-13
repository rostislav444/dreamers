from rest_framework import serializers

from apps.material.models import ProductPart, ProductPartMaterialsGroups, ProductPartMaterials
from apps.material.serializers import ColorSerializer
from apps.product.models import Product3DBlenderModel, ProductClass, Product, Sku, CameraLocations, \
    ProductPartSceneMaterialImage, ProductPartSceneMaterial
from apps.product.serializers.serializers_scene_parts import ProductPartSceneSerializer


class SkuRenderSerializer(serializers.ModelSerializer):
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Sku
        fields = ['id', 'materials']

    @staticmethod
    def get_materials(obj):
        return {material.material.group.product_part.blender_name: material.material.id for material in
                obj.materials.all()}


class CameraLocationsSerializer(serializers.ModelSerializer):
    parts = ProductPartSceneSerializer(many=True, read_only=True)

    class Meta:
        model = CameraLocations
        fields = '__all__'


class ProductRender3DBlenderModelSerializer(serializers.ModelSerializer):
    cameras = CameraLocationsSerializer(many=True, read_only=True)

    class Meta:
        model = Product3DBlenderModel
        fields = ['obj', 'mtl', 'cameras']


class ProductRenderSerializer(serializers.ModelSerializer):
    model_3d = ProductRender3DBlenderModelSerializer(read_only=True)
    parts = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'code', 'model_3d', 'parts']

    def get_parts(self, obj):
        context = self.context.copy()
        context['product_id'] = obj.id

        if obj.product_class.materials_set:
            return ProductPartRenderSerializer(
                obj.product_class.materials_set.parts.all(), many=True, read_only=True, context=context).data


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
    materials = serializers.SerializerMethodField()

    class Meta:
        model = ProductPartMaterialsGroups
        fields = ('product_part', 'type', 'materials',)

    def get_materials(self, obj):
        product = Product.objects.get(id=self.context['product_id'])
        product_part_scene_material = ProductPartSceneMaterial.objects.filter(
            part__camera__model_3d__product=product,
            part__part=obj.product_part,
            image__image__isnull=True
        )

        qs = ProductPartMaterials.objects.filter(
            material_scene__in=product_part_scene_material
        )

        return ProductPartRenderMaterialSerializer(qs, many=True, read_only=True).data


class ProductPartRenderSerializer(serializers.ModelSerializer):
    material_groups = serializers.SerializerMethodField()

    class Meta:
        model = ProductPart
        fields = ('blender_name', 'name', 'material_groups')


    def get_material_groups(self, obj):
        return ProductPartRenderMaterialsGroupsSerializer(obj.material_groups.all(), many=True, read_only=True,
                                                          context=self.context).data


