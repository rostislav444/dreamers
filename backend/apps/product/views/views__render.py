from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import action

from apps.product.models import SkuImages, ProductPartSceneMaterialImage, Product, CameraInteriorLayerMaterialGroup, \
    CameraInteriorLayerMaterialImage, CameraInteriorLayerMaterial
from apps.product.serializers import SkuImagesSerializer, ProductRenderSerializer, ProductInteriorSerializer, \
    CameraInteriorLayerMaterialImageSerializer
from apps.product.serializers.serializers_scene_parts import ProductPartSceneMaterialImageSerializer


class ProductRenderViewSet(generics.GenericAPIView, mixins.RetrieveModelMixin, viewsets.ViewSet):
    serializer_class = ProductRenderSerializer

    def get_queryset(self):
        return Product.objects.all()

    @action(detail=True, methods=['get'])
    def get_all_product_ids(self, request, *args, **kwargs):
        return Product.objects.all().values_list('id', flat=True)


class LoadSkuImageView(generics.GenericAPIView, mixins.CreateModelMixin, viewsets.ViewSet):
    serializer_class = SkuImagesSerializer

    def get_queryset(self):
        return SkuImages.objects.all()

    def create(self, request, *args, **kwargs):
        # Extract values from the request data
        sku = request.data.get('sku')
        index = request.data.get('index')

        # Check if a record with the given sku and index already exists
        existing_object = SkuImages.objects.filter(sku=sku, index=index).first()

        if existing_object:
            # If it exists, delete the old object
            existing_object.delete()

        # Continue with the regular creation process
        return super().create(request, *args, **kwargs)


class LoadProductPartSceneMaterialImageView(generics.GenericAPIView, mixins.CreateModelMixin, viewsets.ViewSet):
    serializer_class = ProductPartSceneMaterialImageSerializer

    def get_queryset(self):
        return ProductPartSceneMaterialImage.objects.all()

    def create(self, request, *args, **kwargs):
        # Extract values from the request data
        scene_material_id = request.data.get('scene_material')
        # Check if a record with the given sku and index already exists
        existing_object = ProductPartSceneMaterialImage.objects.filter(scene_material__id=scene_material_id).first()

        if existing_object:
            # If it exists, delete the old object
            existing_object.delete()

        # Continue with the regular creation process
        return super().create(request, *args, **kwargs)


class RenderInteriorViewSet(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.ViewSet):
    serializer_class = ProductInteriorSerializer

    def get_queryset(self):
        return Product.objects.all()


class LoadInteriorPartImageView(generics.GenericAPIView, mixins.CreateModelMixin, viewsets.ViewSet):
    serializer_class = CameraInteriorLayerMaterialImageSerializer

    def get_queryset(self):
        return CameraInteriorLayerMaterialImage.objects.all()

    def create(self, request, *args, **kwargs):
        # Extract values from the request data
        scene_material_id = request.data.get('scene_material')
        print('CameraInteriorLayerMaterial', CameraInteriorLayerMaterial.objects.get(id=scene_material_id))

        # Check if a record with the given sku and index already exists
        existing_object = CameraInteriorLayerMaterialImage.objects.filter(scene_material__id=scene_material_id).first()

        if existing_object:
            # If it exists, delete the old object
            existing_object.delete()

        # Continue with the regular creation process
        return super().create(request, *args, **kwargs)
