from django.contrib import admin

from apps.product.abstract.admin import FilterAttributeGroupsFK
from apps.product.forms import ProductClassProductAttributesFormSet, ProductClassProductAttributeGroupsForm, ProductClassProductAttributesForm
from apps.product.models import ProductClassProductAttributeGroups, ProductClassProductAttributes


class ProductClassProductAttributeGroupsInline(admin.TabularInline, FilterAttributeGroupsFK):
    model = ProductClassProductAttributeGroups
    form = ProductClassProductAttributeGroupsForm
    show_change_link = True
    extra = 0


class ProductClassProductAttributesInline(admin.TabularInline):
    model = ProductClassProductAttributes
    form = ProductClassProductAttributesForm
    formset = ProductClassProductAttributesFormSet
    extra = 0


@admin.register(ProductClassProductAttributeGroups)
class ProductClassProductAttributeGroupsAdmin(admin.ModelAdmin):
    inlines = [ProductClassProductAttributesInline]
