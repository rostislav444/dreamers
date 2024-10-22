from admin_auto_filters.filters import AutocompleteFilter
from django import forms
from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from apps.abstract.admin import ParentLinkMixin
from apps.material.models import Material, ProductStaticPart, ProductPartMaterialsGroups, ProductPart, \
    ProductPartMaterials, MaterialsSet
from apps.material.forms import ProductStaticPartForm
from apps.material.models.models_material_set import RecommendedCombinations, RecommendedCombinationsParts


class ProductStaticPartInline(admin.StackedInline):
    model = ProductStaticPart
    form = ProductStaticPartForm
    extra = 0

    fields = (('name', 'blender_name', 'group'), 'material', 'color')


class ProductPartMaterialsFilter(AutocompleteFilter):
    title = 'Color'
    field_name = 'color'


@admin.register(ProductPartMaterials)
class ProductPartMaterialsAdmin(admin.ModelAdmin):
    search_fields = ['material__name']


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
        fields = ['material', 'color', 'preferred', 'preview', 'code', ]
        if obj:
            if obj.group.type == 'material':
                fields.remove('color')
            elif obj.group.type == 'color':
                fields.remove('material')
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(self._obj, self._obj.group)
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


# Product part
class ProductPartInline(admin.TabularInline):
    show_change_link = True
    model = ProductPart
    extra = 0


# RecommendedCombinationsParts
class RecommendedCombinationsPartsForm(forms.ModelForm):
    class Meta:
        model = RecommendedCombinationsParts
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'part'):
            self.fields['material'].queryset = ProductPartMaterials.objects.filter(
                group__product_part=self.instance.part)
        else:
            self.fields['material'].queryset = ProductPartMaterials.objects.none()


def get_preview(obj):
    if obj and obj.material:
        if obj.material.color:
            return '<div style="width: 48px; height: 48px; background-color: %s;"></div>' % obj.material.color.hex
        if obj.material.material and obj.material.material.image:
            return '<img src="%s" style="width: 48px; height: 48px; object-fit: cover;" />' % obj.material.material.image.url
    return '-'

class RecommendedCombinationsPartsInline(admin.TabularInline):
    model = RecommendedCombinationsParts
    form = RecommendedCombinationsPartsForm
    readonly_fields = ('preview',)
    fields = ('part', 'material', 'preview')
    extra = 0

    def preview(self, obj):
        return format_html(get_preview(obj))


@admin.register(RecommendedCombinations)
class RecommendedCombinationsAdmin(ParentLinkMixin, admin.ModelAdmin):
    parent_model = MaterialsSet
    inlines = [RecommendedCombinationsPartsInline]
    fields = ['name', 'material_set']


class RecommendedCombinationsInline(admin.TabularInline):
    show_change_link = True
    model = RecommendedCombinations
    readonly_fields = ('preview',)
    fields = ('name', 'preview')
    extra = 0

    def preview(self, obj):
        parts = [
            get_preview(part) for part in obj.parts.all()
        ]
        return format_html('<div style="display: flex;">%s</div>' % ''.join(parts))

@admin.register(ProductPart)
class ProductPartAdmin(admin.ModelAdmin):
    inlines = [ProductPartMaterialsGroupsInline]


@admin.register(MaterialsSet)
class MaterialsSetAdmin(admin.ModelAdmin):
    inlines = [ProductPartInline, RecommendedCombinationsInline]
