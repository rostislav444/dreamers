import abc

from django.contrib import admin

from apps.attribute.models import AttributeGroup
from apps.category.forms import CategoryAttributeGroupFormSet, CategoryAttributeGroupForm
from apps.category.models import Category, Properties, CategoryAttributeGroup


class CategoryAttributeGroupInline(admin.TabularInline):
    model = CategoryAttributeGroup
    formset = CategoryAttributeGroupFormSet
    form = CategoryAttributeGroupForm
    extra = 0

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)
        self._category = None

    # def get_max_num(self, request, obj=None, **kwargs):
    #     ancestors = obj.get_ancestors(include_self=False)
    #     return AttributeGroup.objects.exclude(category_attribute_groups__category__in=ancestors).count()
    #
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "attribute_group" and self._category:
    #         ancestors = self._category.get_ancestors(include_self=False)
    #         kwargs["queryset"] = AttributeGroup.objects.exclude(category_attribute_groups__category__in=ancestors)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
    #
    # def get_formset(self, request, obj=None, **kwargs):
    #     self._category = obj
    #     return super(CategoryAttributeGroupInline, self).get_formset(request, obj, **kwargs)


class PropertiesInline(admin.TabularInline):
    model = Properties
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryAttributeGroupInline,
    ]
