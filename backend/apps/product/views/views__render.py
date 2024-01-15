from rest_framework import viewsets, mixins, generics

from apps.product.models import ProductClass, SkuImages
from apps.product.serializers import SkuImagesSerializer, ProductRenderWithSkuSerializer


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


class ProductClassRenderViewSet(generics.GenericAPIView, mixins.RetrieveModelMixin, viewsets.ViewSet):
    serializer_class = ProductRenderWithSkuSerializer

    def get_queryset(self):
        return ProductClass.objects.all()
