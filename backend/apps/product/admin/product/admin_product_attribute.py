from django.contrib import admin

from apps.product.forms import ProductAttributeFormSet, ProductAttributeForm
from apps.product.models import ProductAttribute


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    form = ProductAttributeForm
    formset = ProductAttributeFormSet

    def get_min_num(self, request, obj=None, **kwargs):
        return obj.product_class.product_attributes_groups.count()

    def get_max_num(self, request, obj=None, **kwargs):
        return obj.product_class.product_attributes_groups.count()
