from django.contrib import admin

from apps.attribute.abstract.admin import AttributeFildSet
from apps.attribute.abstract.fields import OptionGroupField
from apps.attribute.models import Attribute
from apps.product.abstract.admin import FilterAttributeGroupsFK, ReturnToProductClassAdmin
from apps.product.forms import ProductClassOptionGroupForm, ProductClassOptionCustomGroupForm, \
    ProductClassOptionCustomGroupFormSet, \
    ProductClassOptionGroupFormSet
from apps.product.models import ProductClassOptionGroup, ProductClassOption


# Product Class Option
class ProductClassOptionInline(AttributeFildSet):
    model = ProductClassOption
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "value_attribute":
            parent_id = request.resolver_match.kwargs.get('object_id')
            kwargs["queryset"] = Attribute.objects.filter(attribute_group__product_class_option_group=parent_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProductClassOptionGroup)
class ProductClassOptionGroupAdmin(ReturnToProductClassAdmin, admin.ModelAdmin):
    inlines = [ProductClassOptionInline]

    def get_fieldsets(self, request, obj=None):
        if obj.type == OptionGroupField.ATTRIBUTE:
            return (None, {
                'fields': (
                'product_class_link', ('type', 'attribute_group'), ('save_all_options', 'image_dependency'),),
            }),
        return (None, {
            'fields': ('product_class_link', ('type', 'name'), 'image_dependency',),
        }),

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        for inline in super(ProductClassOptionGroupAdmin, self).get_inline_instances(request, obj):
            if inline.model.__name__ == ProductClassOption.__name__:
                if not obj.attribute_group or obj.attribute_group and not obj.attribute_group.custom:
                    inline_instances.append(inline)
        return obj and inline_instances or []


class ProductClassOptionGroupInline(admin.TabularInline, FilterAttributeGroupsFK):
    model = ProductClassOptionGroup
    form = ProductClassOptionGroupForm
    formset = ProductClassOptionGroupFormSet
    show_change_link = True
    extra = 0
    fields = ('type', 'attribute_group', 'model_3d_name', 'image_dependency', 'save_all_options')


class ProductClassOptionGroupCustomInline(admin.TabularInline):
    model = ProductClassOptionGroup
    form = ProductClassOptionCustomGroupForm
    formset = ProductClassOptionCustomGroupFormSet
    show_change_link = True
    extra = 0
    fields = ('type', 'name', 'unit', 'image_dependency')
