from django.db.models import Prefetch, Q
from rest_framework import viewsets, mixins, generics

from apps.attribute.abstract.fields import AttributeGroupTypeField
from apps.attribute.models import AttributeGroup, Attribute, AttributeColor
from apps.attribute.serializers import AttributeGroupLiteSerializer
from apps.category.models import Category


class AttributesViewSet(generics.GenericAPIView, mixins.ListModelMixin, viewsets.ViewSet):
    serializer_class = AttributeGroupLiteSerializer
    categories = Category.objects.none()

    @staticmethod
    def filter_attributes_byt_category(categories):
        return Attribute.objects.prefetch_related(
            'product_class_options',
            'product_class_options__attribute_group',
            'product_class_options__attribute_group__product_class',
            'product_class_options__attribute_group__product_class__category',
            'product_class_attributes',
            'product_class_attributes__product_attributes',
            'product_class_attributes__product_attributes__product',
            'product_class_attributes__product_attributes__product__product_class',
            'product_class_attributes__product_attributes__product__product_class__category'
        ).filter(
            Q(productclassattributes__product_class__category__in=categories) |
            Q(product_class_options__attribute_group__product_class__category__in=categories) |
            Q(product_class_attributes__product_attributes__product__product_class__category__in=categories)
        ).exclude(
            attribute_group__type__in=[AttributeGroupTypeField.COLOR, AttributeGroupTypeField.IMAGE]
        ).distinct()

    @staticmethod
    def filter_colors_byt_category(categories):
        return AttributeColor.objects.filter(
            attributes__product_class_options__attribute_group__product_class__category__in=categories
        ).distinct()

    def get_queryset(self):
        self.categories = Category.objects.get(name="Мебель").get_family()
        attributes = self.filter_attributes_byt_category(self.categories)
        colors = self.filter_colors_byt_category(self.categories)

        return AttributeGroup.objects.filter(
            category__in=self.categories,
            attributes__isnull=False
        ).exclude(
            product_class_option_group__image_dependency=False
        ).prefetch_related(
            Prefetch('attributes', queryset=attributes),
            Prefetch('colors', queryset=colors)
        ).distinct()
