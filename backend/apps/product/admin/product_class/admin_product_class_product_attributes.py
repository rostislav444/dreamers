from django.contrib import admin

from apps.product.abstract.admin import FilterAttributeGroupsFK
from apps.product.forms import ProductClassProductAttributeGroupsForm, ProductClassProductAttributesFormSet, \
    ProductClassProductAttributesForm
from apps.product.models import ProductClassProductAttributeGroups, ProductClassProductAttributes


class ProductClassProductAttributeGroupsInline(admin.TabularInline, FilterAttributeGroupsFK):
    model = ProductClassProductAttributeGroups
    form = ProductClassProductAttributeGroupsForm
    show_change_link = True
    extra = 0


class ProductClassProductAttributesInline(admin.TabularInline):
    model = ProductClassProductAttributes
    form = ProductClassProductAttributesForm
    # formset = ProductClassProductAttributesFormSet
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                'value_text', 'value_integer', 'value_boolean', 'value_float',
                'value_color_name',
                'value_color_hex', 'value_color_image', 'value_image_name', 'value_image_image',
                ('value_min', 'value_max',),)
        },),
    )

    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = super(ProductClassProductAttributesInline, self).get_fieldsets(request, obj)
    #     fields = []
    #     if obj:
    #         fields += obj.attribute_group.actual_field_name
    #
    #     print(fields)
    #
    #     fieldsets[0][1]['fields'] = fields
    #     return fieldsets

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "value_attribute":
    #         parent_id = request.resolver_match.kwargs.get('object_id')
    #         kwargs["queryset"] = Attribute.objects.filter(attribute_group__product_class_option_group=parent_id)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProductClassProductAttributeGroups)
class ProductClassProductAttributeGroupsAdmin(admin.ModelAdmin):
    inlines = [ProductClassProductAttributesInline]
