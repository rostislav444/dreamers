from rest_framework import viewsets, mixins, generics

from apps.catalogue.serializers import CatalogueProductSerializer
from apps.product.models import Product


class CatalogueProductViewSet(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                              viewsets.ViewSet):
    serializer_class = CatalogueProductSerializer

    def get_queryset(self):
        return Product.objects.all().prefetch_related('product_class__materials_set__parts')
