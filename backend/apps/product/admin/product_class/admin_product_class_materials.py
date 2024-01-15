from django.contrib import admin
from django.utils.html import format_html
from admin_auto_filters.filters import AutocompleteFilter
from apps.material.models import Material
from apps.product.forms.product_class.forms_product_class_parts import ProductStaticPartForm
from apps.product.models import ProductStaticPart, ProductPartMaterialsGroups, ProductPart, ProductPartMaterials


class ProductStaticPartInline(admin.StackedInline):
    model = ProductStaticPart
    form = ProductStaticPartForm
    extra = 0

    fields = (('name', 'blender_name', 'group'), 'material', 'color')


class ProductPartMaterialsFilter(AutocompleteFilter):
    title = 'Color'
    field_name = 'color'


class ProductPartMaterialsInline(admin.TabularInline):
    _obj = None

    model = ProductPartMaterials
    readonly_fields = ('code', 'preview')
    list_filter = [ProductPartMaterialsFilter]
    search_fields = ['color__name']
    autocomplete_fields = ['color']
    extra = 0

    def preview(self, obj):
        if obj:
            if obj.color:
                return format_html('<div style="width: 48px; height: 48px; background-color: {};"></div>',
                                   obj.color.hex)
            if obj.material and obj.material.image:
                return format_html('<img src="{}" style="width: 48px; height: 48px; object-fit: cover;" />',
                                   obj.material.image.url)
        return '-'

    def get_fields(self, request, obj=None):
        self._obj = obj
        fields = ['material', 'color', 'show_in_catalogue', 'preview', 'code', ]
        if obj:
            if obj.group.type == 'material':
                fields.remove('color')
            elif obj.group.type == 'color':
                fields.remove('material')
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'material':
            kwargs['queryset'] = Material.objects.filter(group=self._obj.group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProductPartMaterialsGroups)
class ProductPartMaterialsGroupsAdmin(admin.ModelAdmin):
    inlines = [
        ProductPartMaterialsInline,
    ]

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        if obj and obj.group.type == 'material' or not obj:
            fields = [field for field in fields if field != 'add_palette']

        return fields


class ProductPartMaterialsGroupsInline(admin.TabularInline):
    show_change_link = True
    model = ProductPartMaterialsGroups
    extra = 0


'''Product part'''


class ProductPartInline(admin.TabularInline):
    show_change_link = True
    model = ProductPart
    extra = 0


@admin.register(ProductPart)
class ProductPartAdmin(admin.ModelAdmin):
    inlines = [ProductPartMaterialsGroupsInline]
