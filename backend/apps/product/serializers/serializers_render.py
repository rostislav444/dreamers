from rest_framework import serializers

from apps.material.models import ProductPart, ProductPartMaterialsGroups, ProductPartMaterials
from apps.material.serializers import ColorSerializer
from apps.material.serializers.serializers_materials import BlenderMaterialSerializer, Material3DSerializer
from apps.product.models import Product3DBlenderModel, ProductClass, Product, Sku, Camera, \
    ProductPartSceneMaterialImage, ProductPartSceneMaterial, CameraInteriorLayer, CameraInteriorLayerMaterial, \
    CameraInteriorLayerMaterialImage
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


class ProductCameraInteriorLayerMaterialImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraInteriorLayerMaterialImage
        fields = ['image', 'image_thumbnails']


class ProductCameraInteriorLayerSerializer(serializers.ModelSerializer):
    materials = serializers.SerializerMethodField()

    class Meta:
        model = CameraInteriorLayer
        fields = ['materials']

    @staticmethod
    def get_materials(obj):
        qs = CameraInteriorLayerMaterialImage.objects.filter(scene_material__group__layer=obj)
        return ProductCameraInteriorLayerMaterialImageSerializer(qs, many=True, read_only=True).data


class CameraSerializer(serializers.ModelSerializer):
    interior_layers = ProductCameraInteriorLayerSerializer(many=True, read_only=True)
    parts = ProductPartSceneSerializer(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = ['id', 'pos_x', 'pos_y', 'pos_z', 'rad_x', 'rad_y', 'rad_z', 'interior_layers', 'parts']


class ProductRender3DBlenderModelSerializer(serializers.ModelSerializer):
    cameras = CameraSerializer(many=True, read_only=True)

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
    material = Material3DSerializer(read_only=True)

    class Meta:
        model = ProductPartMaterials
        fields = ('id', 'color', 'material',)


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
            # image__image__isnull=True
        )
        qs = ProductPartMaterials.objects.filter(
            material_scene__in=product_part_scene_material
        )
        serializer = ProductPartRenderMaterialSerializer(qs, many=True, read_only=True,
                                                         context={'request': self.context['request']})
        return serializer.data


class ProductPartRenderSerializer(serializers.ModelSerializer):
    material_groups = serializers.SerializerMethodField()

    class Meta:
        model = ProductPart
        fields = ('blender_name', 'name', 'material_groups')

    def get_material_groups(self, obj):
        return ProductPartRenderMaterialsGroupsSerializer(obj.material_groups.all(), many=True, read_only=True,
                                                          context=self.context).data
