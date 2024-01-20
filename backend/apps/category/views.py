from rest_framework import viewsets, mixins, generics

from apps.category.models import Category
from apps.category.serializers import NestedCategorySerializer


class NestedCategoryView(generics.GenericAPIView, mixins.ListModelMixin, viewsets.ViewSet):
    serializer_class = NestedCategorySerializer

    def get_queryset(self):
        categories = self.request.GET.get('categories')
        if categories:
            categories = categories.split(',')
            if len(categories) > 1:
                return Category.objects.filter(parent__slug=categories[-2], slug=categories[-1])
            return Category.objects.filter(slug=categories[-1])
        return Category.objects.filter(level=0)
