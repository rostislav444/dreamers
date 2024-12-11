from django.http import JsonResponse
from django.core.cache import cache
from rest_framework import viewsets, mixins, generics
from django.conf import settings
from rest_framework.response import Response

from apps.product.models import Product
from apps.product.serializers import ProductSerializer


class ProductViewSet(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.ViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'code'
    cache_timeout = 60 * 60 * 24

    def get_queryset(self):
        return Product.objects.all()

    def get_list_cache_key(self):
        return 'product_list_all'

    def get_detail_cache_key(self, code):
        return f'product_detail_{code}'

    def list(self, request, *args, **kwargs):
        cache_key = self.get_list_cache_key()
        result = cache.get(cache_key)

        if result is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, self.cache_timeout)
            return response

        return Response(result)

    def retrieve(self, request, *args, **kwargs):
        code = kwargs.get(self.lookup_field)
        cache_key = self.get_detail_cache_key(code)
        result = cache.get(cache_key)

        if result is None:
            response = super().retrieve(request, *args, **kwargs)
            cache.set(cache_key, response.data, self.cache_timeout)
            return response

        return Response(result)


def products_list(request):
    cache_key = 'products_codes_list'
    result = cache.get(cache_key)

    if result is None:
        data = Product.objects.all().values_list('code', flat=True)
        result = {'products': list(data)}
        cache.set(cache_key, result, 60 * 15)  # cache for 15 minutes

    return JsonResponse(result)