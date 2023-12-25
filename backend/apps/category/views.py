from rest_framework import viewsets, mixins, generics

from apps.category.models import Category
from apps.category.serializers import NestedCategorySerializer


class NestedCategoryView(generics.GenericAPIView, mixins.ListModelMixin, viewsets.ViewSet):
    serializer_class = NestedCategorySerializer

    def get_queryset(self):
        return Category.objects.filter(level=0)
