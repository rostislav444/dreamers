from django.contrib import admin
from apps.interior.models import Interior, InteriorLayer, InteriorLayerMaterialGroup, InteriorMaterial
from django.utils.html import format_html

from apps.material.models import Material


class InteriorMaterialInline(admin.TabularInline):
    _obj = None
    model = InteriorMaterial
    show_change_link = True
    extra = 0

    readonly_fields = ('id', 'preview')
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
        fields = ['material', 'color', 'preview',]
        if obj:
            if obj.material_group.type == 'material':
                fields.remove('color')
            elif obj.material_group.type == 'color':
                fields.remove('material')
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(self._obj, self._obj.material_group)
        if db_field.name == 'material':
            kwargs['queryset'] = Material.objects.filter(group=self._obj.material_group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(InteriorLayerMaterialGroup)
class InteriorLayerMaterialGroupAdmin(admin.ModelAdmin):
    inlines = [InteriorMaterialInline]


class InteriorLayerMaterialGroupInline(admin.TabularInline):
    model = InteriorLayerMaterialGroup
    show_change_link = True
    extra = 0


@admin.register(InteriorLayer)
class InteriorLayerAdmin(admin.ModelAdmin):
    inlines = [InteriorLayerMaterialGroupInline]


class InteriorLayerInline(admin.TabularInline):
    model = InteriorLayer
    show_change_link = True
    extra = 0


@admin.register(Interior)
class InteriorAdmin(admin.ModelAdmin):
    inlines = [InteriorLayerInline]
