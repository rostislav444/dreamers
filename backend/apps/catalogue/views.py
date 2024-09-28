from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics

from apps.catalogue.serializers import CatalogueProductSerializer
from apps.category.models import Category
from apps.product.models import Product


class CatalogueProductViewSet(generics.GenericAPIView,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.ViewSet):
    serializer_class = CatalogueProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        final_category = self.get_final_category(self.request.GET.get('categories'))

        if final_category:
            queryset = queryset.filter(product_class__category=final_category)

        return self.apply_prefetch_related(queryset)

    @staticmethod
    def get_final_category(categories):
        if not categories:
            return None

        slugs = categories.split(',')
        final_category = None
        for slug in slugs:
            final_category = get_object_or_404(Category, slug=slug, parent__slug=final_category)

        return final_category

    @staticmethod
    def apply_prefetch_related(queryset):
        return queryset.select_related(
            'product_class__category'
        ).prefetch_related(
            'product_class__materials_set__parts'
        )
