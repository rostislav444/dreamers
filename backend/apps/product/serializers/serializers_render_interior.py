from rest_framework import serializers

from apps.interior.serializers import InteriorMaterialSerializer
from apps.product.models import Product, Product3DBlenderModel, Camera, CameraInteriorLayer, \
    CameraInteriorLayerMaterialGroup, CameraInteriorLayerMaterial, CameraInteriorLayerMaterialImage

class CameraInteriorLayerMaterialImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraInteriorLayerMaterialImage
        fields = ['id', 'scene_material', 'image']
        read_only_fields = ['id']


class CameraInteriorLayerMaterialSerializer(serializers.ModelSerializer):
    material = InteriorMaterialSerializer(read_only=True)

    class Meta:
        model = CameraInteriorLayerMaterial
        fields = ['id', 'material']


class CameraInteriorLayerMaterialGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='material_group.material_group.name', read_only=True)
    materials = CameraInteriorLayerMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = CameraInteriorLayerMaterialGroup
        fields = ['id', 'name', 'materials']


class CameraInteriorLayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='interior_layer.name', read_only=True)
    slug = serializers.CharField(source='interior_layer.slug', read_only=True)
    material_groups = CameraInteriorLayerMaterialGroupSerializer(many=True, read_only=True)

    class Meta:
        model = CameraInteriorLayer
        fields = ['id', 'name', 'slug', 'material_groups']


class ProductInteriorCameraSerializer(serializers.ModelSerializer):
    interior_layers = CameraInteriorLayerSerializer(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = ['id', 'pos_x', 'pos_y', 'pos_z', 'rad_x', 'rad_y', 'rad_z', 'interior_layers']


class ProductInteriorProduct3DBlenderModelSerializer(serializers.ModelSerializer):
    cameras = ProductInteriorCameraSerializer(many=True, read_only=True)

    class Meta:
        model = Product3DBlenderModel
        fields = ['obj', 'mtl', 'cameras']


class ProductInteriorSerializer(serializers.ModelSerializer):
    model_3d = ProductInteriorProduct3DBlenderModelSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'code', 'model_3d', 'width', 'height', 'depth']
