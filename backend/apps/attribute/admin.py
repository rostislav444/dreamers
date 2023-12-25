from django import forms
from django.contrib import admin
from django.db import models
from django_admin_inline_paginator.admin import TabularInlinePaginated

from apps.abstract.admin import ParentLinkMixin
from apps.attribute.abstract.admin import AttributeFildSet
from apps.attribute.forms import AttributeInlineForm
from apps.attribute.models import AttributeGroupUnit, AttributeGroup, AttributeSubGroup, AttributeUnitGroup, \
    AttributeUnit, Attribute


# Attribute Group Unit
@admin.register(AttributeGroupUnit)
class AttributeGroupUnitAdmin(admin.ModelAdmin):
    list_display = ['name']


# Attribute Unit Group
class AttributeUnitInline(AttributeFildSet):
    model = AttributeUnit
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        self.object = obj
        if not obj or obj.custom:
            return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "attribute":
            parent_id = request.resolver_match.kwargs.get('object_id')
            kwargs["queryset"] = Attribute.objects.filter(group__unit_group=parent_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(AttributeUnitGroup)
class AttributeUnitGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'group']
    inlines = [AttributeUnitInline]


class AttributeUnitGroupInline(admin.StackedInline):
    show_change_link = True
    model = AttributeUnitGroup
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj or obj.custom:
            return 0


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'attribute_group']


class AttributeInline(AttributeFildSet, TabularInlinePaginated):
    model = Attribute
    form = AttributeInlineForm
    per_page = 10
    can_delete = True
    extra = 0

    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '16'})},
    }

    def __init__(self, *args, **kwargs):
        self.object = None
        super(AttributeInline, self).__init__(*args, **kwargs)

    def get_max_num(self, request, obj=None, **kwargs):
        if isinstance(obj, AttributeSubGroup):
            obj = obj.group

        self.object = obj
        if not obj or obj.custom:
            return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if self.object and db_field.name == "sub_group":
            kwargs["queryset"] = self.object.sub_groups.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Attribute Sub Group
@admin.register(AttributeSubGroup)
class AttributeSubGroupAdmin(ParentLinkMixin, admin.ModelAdmin):
    parent_model = AttributeGroup

    inlines = [
        AttributeInline
    ]
    fieldset = [[None, {
        'fields': ['name', 'group']
    }]]

    def get_fieldsets(self, request, obj=None):
        fieldset = super(AttributeSubGroupAdmin, self).get_fieldsets(request, obj)

        if obj.group.price_required == AttributeGroup.PRICE_RQ_SUB_GROUP:
            if 'price' not in fieldset[0][1]['fields']:
                fieldset[0][1]['fields'].append('price')
        return fieldset


class AttributeSubGroupInline(admin.StackedInline):
    show_change_link = True
    model = AttributeSubGroup
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj or obj.custom:
            return 0


@admin.register(AttributeGroup)
class AttributeGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    inlines = [
        AttributeSubGroupInline,
        AttributeUnitGroupInline,
        AttributeInline
    ]
