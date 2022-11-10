from rest_framework import viewsets, mixins, generics

from apps.product.models import ProductClass
from apps.product.serializers import ProductClassSerializer
from apps.attribute.models import AttributeGroup
from django.db.models import OuterRef, Subquery, JSONField


class ProductClassViewSet(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.ViewSet):
    serializer_class = ProductClassSerializer

    def get_queryset(self):
        qs = ProductClass.objects.all()
        return qs

