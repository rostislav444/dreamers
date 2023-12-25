from django.contrib import admin
from django_admin_inline_paginator.admin import TabularInlinePaginated

from apps.abstract.admin import ParentLinkMixin
from apps.attribute.abstract import attr_fields
from apps.attribute.abstract.admin import AttributeFildSet
from apps.attribute.abstract.fields import OptionGroupField
from apps.attribute.models import Attribute
from apps.product.abstract.admin import FilterAttributeGroupsFK
from apps.product.forms import ProductClassOptionGroupForm, ProductClassOptionCustomGroupForm, \
    ProductClassOptionCustomGroupFormSet, \
    ProductClassOptionGroupFormSet
from apps.product.models import ProductClassOptionGroup, ProductClassOption, ProductClass


# Group inline for Product Class
class ProductClassOptionGroupInline(admin.TabularInline, FilterAttributeGroupsFK):
    model = ProductClassOptionGroup
    form = ProductClassOptionGroupForm
    formset = ProductClassOptionGroupFormSet
    show_change_link = True
    extra = 0
    fields = ('type', 'attribute_group', 'w', 'h', 'd', 'model_3d_name', 'image_dependency')


# Product Class Option
class ProductClassOptionInline(AttributeFildSet, TabularInlinePaginated):
    _object = None
    model = ProductClassOption
    extra = 0
    can_delete = True

    def __init__(self, parent_model, admin_site, sub_group=None):
        self.sub_group = sub_group
        if sub_group:
            self.verbose_name_plural = sub_group.name
        super(ProductClassOptionInline, self).__init__(parent_model, admin_site)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(value_attribute__sub_group=self.sub_group)

    def get_max_num(self, request, obj=None, **kwargs):
        self._object = obj
        if not obj:
            return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "value_attribute":
            parent_id = request.resolver_match.kwargs.get('object_id')
            kwargs["queryset"] = Attribute.objects.filter(
                attribute_group__product_class_option_group=parent_id,
                sub_group=self.sub_group
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None, **kwargs):
        fieldsets = super(ProductClassOptionInline, self).get_fieldsets(request, obj)
        fields = ['attribute_group']

        if obj.type == OptionGroupField.ATTRIBUTE:
            fields.append('value_attribute')
        else:
            fields = [*fields, *attr_fields[obj.type]]

        if obj.option_price_required:
            fields.append('price')

        fieldsets[0][1]['fields'] = fields
        return fieldsets


@admin.register(ProductClassOptionGroup)
class ProductClassOptionGroupAdmin(ParentLinkMixin, admin.ModelAdmin):
    _object = None
    parent_model = ProductClass

    def get_inline_instances(self, request, obj=None):
        sub_groups = [*obj.attribute_sub_group.all(), None]
        return [ProductClassOptionInline(self.model, self.admin_site, sub_group) for sub_group in sub_groups]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'attribute_sub_group' and self._object:
            kwargs["queryset"] = self._object.attribute_group.sub_groups.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        self._object = obj

        if obj.type == OptionGroupField.ATTRIBUTE:
            return (None, {
                'fields': [
                    'parent_link', 'type', 'attribute_group', 'attribute_sub_group',
                    ('use_all_options', 'option_price_required',),
                    'image_dependency',
                ],
            }),
        return (None, {
            'fields': ['parent_link', ('type', 'name'), 'option_price_required', 'image_dependency', ],
        }),


class ProductClassOptionGroupCustomInline(admin.TabularInline):
    model = ProductClassOptionGroup
    form = ProductClassOptionCustomGroupForm
    formset = ProductClassOptionCustomGroupFormSet
    show_change_link = True
    extra = 0
    fields = ('type', 'name', 'unit', 'image_dependency')
