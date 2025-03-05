from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics, pagination
from rest_framework.response import Response
from django.conf import settings

from apps.catalogue.serializers import CatalogueProductSerializer
from apps.category.models import Category
from apps.product.models import Product
from apps.core.pagination import StandardResultsSetPagination


class CatalogueProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CatalogueProductSerializer
    pagination_class = StandardResultsSetPagination
    CACHE_TTL = 60 * 15  # 15 минут
    
    def get_queryset(self):
        categories = self.request.query_params.get('categories', '')
        
        # Include pagination info in cache key
        page = self.request.query_params.get('page', '1')
        page_size = self.request.query_params.get('page_size', '24')
        cache_key = f'catalogue_products_{categories}_{page}_{page_size}'

        # Try to get from cache
        queryset = cache.get(cache_key)

        if queryset is None:
            # If not in cache, execute query
            queryset = Product.objects.all()
            final_category = self.get_final_category(categories)

            if final_category:
                queryset = queryset.filter(product_class__category=final_category)

            queryset = self.apply_prefetch_related(queryset)

            # Save to cache
            cache.set(cache_key, queryset, self.CACHE_TTL)

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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