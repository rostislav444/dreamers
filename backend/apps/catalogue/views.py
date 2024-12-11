from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics
from django.conf import settings

from apps.catalogue.serializers import CatalogueProductSerializer
from apps.category.models import Category
from apps.product.models import Product


class CatalogueProductViewSet(generics.GenericAPIView,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.ViewSet):
    serializer_class = CatalogueProductSerializer
    CACHE_TTL = 60 * 15  # 15 минут

    def get_queryset(self):
        categories = self.request.GET.get('categories', '')
        cache_key = f'catalogue_products_{categories}'

        # Пробуем получить данные из кеша
        queryset = cache.get(cache_key)
        print('queryset', queryset)

        if queryset is None:
            # Если в кеше нет, выполняем запрос
            queryset = Product.objects.all()
            final_category = self.get_final_category(categories)

            if final_category:
                queryset = queryset.filter(product_class__category=final_category)

            queryset = self.apply_prefetch_related(queryset)

            # Сохраняем в кеш
            cache.set(cache_key, queryset, self.CACHE_TTL)

        return queryset

    @staticmethod
    def get_final_category(categories):
        if not categories:
            return None

        cache_key = f'category_tree_{categories}'
        final_category = cache.get(cache_key)

        if final_category is None:
            slugs = categories.split(',')
            final_category = None
            for slug in slugs:
                final_category = get_object_or_404(Category, slug=slug, parent__slug=final_category)

            cache.set(cache_key, final_category, 60 * 30)  # кешируем на 30 минут

        return final_category

    @staticmethod
    def apply_prefetch_related(queryset):
        return queryset.select_related(
            'product_class__category'
        ).prefetch_related(
            'product_class__materials_set__parts'
        )