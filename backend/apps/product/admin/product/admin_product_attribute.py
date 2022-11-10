from django.contrib import admin

from apps.product.forms import ProductAttributeFormSet, ProductAttributeForm
from apps.product.models import ProductAttribute


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    form = ProductAttributeForm
    formset = ProductAttributeFormSet
    # fieldsets = (
    #     (None, {
    #         'fields': (
    #             'attribute_group', 'value_attribute', 'value_text', 'value_integer', 'value_boolean', 'value_float', 'value_color_name',
    #             'value_color_hex', 'value_color_image', 'value_image_name', 'value_image_image',
    #             ('value_min', 'value_max',),)
    #     },),
    # )

    # @staticmethod
    # def get_max_num_count(obj):
    #     if not obj:
    #         return 0
    #     return obj.product_class.product_attributes.count()
    #
    # def get_max_num(self, request, obj=None, **kwargs):
    #     return self.get_max_num_count(obj)
    #
    # def get_extra(self, request, obj=None, **kwargs):
    #     return self.get_max_num_count(obj)
    #
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "attribute_group":
    #         object_id = request.resolver_match.kwargs.get('object_id')
    #         product = Product.objects.get(id=object_id)
    #         product_class = product.product_class
    #         # attgipu_grpoups_ids = obj.product_class.product_attributes.all().values_list('attribute_group', flat=True)
    #         # kwargs["queryset"] = product_class
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
