from rest_framework import viewsets, mixins, generics

from apps.product.models import Product
from apps.product.serializers import ProductSerializer


class ProductViewSet(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.ViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()








