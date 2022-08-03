from django.contrib import admin
from apps.category.models import Category, Properties
from apps.attribute.models import AttributeGroup


class AttributeGroupInline(admin.TabularInline):
    show_change_link = True
    model = AttributeGroup
    extra = 0


class PropertiesInline(admin.TabularInline):
    model = Properties
    extra = 0


@admin.register(Category)
class CategroyAdmin(admin.ModelAdmin):
    inlines = [
        AttributeGroupInline,
        PropertiesInline
    ]