from apps.product.abstract.admin import FilterAttributeGroupsFK
from apps.product.forms import ProductClassAttributesForm
from apps.product.models import ProductClassAttributes


class ProductClassAttributesInline(FilterAttributeGroupsFK):
    model = ProductClassAttributes
    form = ProductClassAttributesForm
    extra = 0
    # fieldsets = (
    #     (None, {
    #         'fields': (
    #             'attribute_group', 'value_attribute', 'value_text', 'value_integer', 'value_boolean', 'value_float',
    #             'value_color_name',
    #             'value_color_hex', 'value_color_image', 'value_image_name', 'value_image_image',
    #             ('value_min', 'value_max',),)
    #     },),
    # )