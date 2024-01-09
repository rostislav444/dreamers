from rest_framework import viewsets, mixins, generics

from apps.product.models import ProductClass, SkuImages
from apps.product.serializers import SkuImagesSerializer, ProductRenderWithSkuSerializer


class SkuImageLoadView(generics.GenericAPIView, mixins.CreateModelMixin, viewsets.ViewSet):
    serializer_class = SkuImagesSerializer

    def get_queryset(self):
        return SkuImages.objects.all()



class ProductClassRenderViewSet(generics.GenericAPIView, mixins.RetrieveModelMixin, viewsets.ViewSet):
    serializer_class = ProductRenderWithSkuSerializer

    def get_queryset(self):
        return ProductClass.objects.all()