from django_filters.rest_framework import FilterSet
import django_filters

from apps.product.models import Product


class ProductFilter(FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('name', 'price', 'category')