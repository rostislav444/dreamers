from django.db.models import Prefetch
from django.http import JsonResponse
from rest_framework import viewsets, mixins, generics

from apps.product.models import Product, Sku
from apps.product.serializers import ProductSerializer


class ProductViewSet(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.ViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'code'

    def get_queryset(self):
        return Product.objects.all()
        # return Product.objects.all().prefetch_related(
        #     Prefetch('sku', Sku.objects.filter(images__isnull=False))
        # )


def products_list(request):
    data = Product.objects.all().values_list('code', flat=True)
    json_data = {'products': list(data)}
    return JsonResponse(json_data)
