from django.db.models import Prefetch, Q
from rest_framework import viewsets, mixins, generics

from apps.product.models import ProductClass, ProductClassProductAttributes, ProductClassOption
from apps.product.serializers import ProductClassSerializer


class ProductClassViewSet(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.ViewSet):
    serializer_class = ProductClassSerializer

    def get_queryset(self):
        qs = ProductClass.objects.all().prefetch_related(
            Prefetch('product_attributes_groups__attributes',
                     queryset=ProductClassProductAttributes.objects.filter(product_attributes__isnull=False)),
        )
        return qs
