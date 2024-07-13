from rest_framework import viewsets, mixins, generics

from apps.product.models import SkuImages, ProductPartSceneMaterialImage, Product
from apps.product.serializers import SkuImagesSerializer, ProductRenderSerializer
from apps.product.serializers.serializers_scene_parts import ProductPartSceneMaterialImageSerializer


class ProductRenderViewSet(generics.GenericAPIView, mixins.RetrieveModelMixin, viewsets.ViewSet):
    serializer_class = ProductRenderSerializer

    def get_queryset(self):
        return Product.objects.all()


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
