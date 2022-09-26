from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from apps.attribute.serializers import AttributeGroupSerializer
from apps.attribute.models import AttributeGroup
from apps.category.models import Category
from apps.product.models import ProductClass, Product


class AttributesViewSet(generics.GenericAPIView, mixins.ListModelMixin, viewsets.ViewSet):
    serializer_class = AttributeGroupSerializer

    def get_queryset(self):
        products_classes = ProductClass.objects.all()

        return AttributeGroup.objects.all()
