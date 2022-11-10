from django.db.models import Prefetch, Q
from rest_framework import viewsets, mixins, generics

from apps.attribute.models import AttributeGroup, Attribute
from apps.attribute.serializers import AttributeGroupLiteSerializer
from apps.category.models import Category


class AttributesViewSet(generics.GenericAPIView, mixins.ListModelMixin, viewsets.ViewSet):
    serializer_class = AttributeGroupLiteSerializer
    categories = Category.objects.none()

    @staticmethod
    def filter_attributes_byt_category(categories):
        return Attribute.objects.filter(
            Q(productclassattributes__product_class__category__in=categories) |
            Q(productclassoption__attribute_group__product_class__category__in=categories) |
            Q(product_attributes__product__product_class__category__in=categories)
        ).distinct()

    def get_queryset(self):
        self.categories = Category.objects.get(name="Мебель").get_family()
        attributes = self.filter_attributes_byt_category(self.categories)
        attributes_groups = attributes.values_list('attribute_group', flat=True)
        return AttributeGroup.objects.filter(id__in=attributes_groups).prefetch_related(
            Prefetch('attributes', queryset=attributes))
