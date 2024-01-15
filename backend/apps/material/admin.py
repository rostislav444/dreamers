from django.contrib import admin
from django.utils.html import format_html

from apps.material.models import MaterialGroups, MaterialSubGroup, Material, Color, BaseColor, BlenderMaterial, Palette, \
    PaletteColor


@admin.register(BlenderMaterial)
class BlenderMaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(BaseColor)
class BaseColorAdmin(admin.ModelAdmin):
    @staticmethod
    def color_preview(obj):
        if obj.hex:
            return format_html('''<div style="
                width: 48px; 
                height: 48px; 
                background-color: {}; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            "></div>''', obj.hex)
        return '-'

    list_display = ('color_preview', 'name', 'lvl', 'index', 'hex',)
    readonly_fields = ('color_preview',)



class PaletteColorInline(admin.TabularInline):
    model = PaletteColor
    extra = 0


@admin.register(Palette)
class PaletteAdmin(admin.ModelAdmin):
    def colors(self, obj):
        data = []
        for hex_color in obj.colors.all().order_by('color__ral').values_list('color__hex', flat=True):
            data.append(f'<div style="background-color: {hex_color}; width: 48px; height: 48px; margin: 2px;"></div>')
        return format_html('<div style="display: grid; grid-template-columns: repeat(auto-fill, 48px); gap: 4px;">' + ''.join(
            data) + '</div>')

    inlines = [PaletteColorInline]
    list_display = ('name', 'colors',)
    readonly_fields = ('colors',)



@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    @staticmethod
    def color_preview(obj):
        if obj.hex:
            return format_html('''<div style="
                width: 48px; 
                height: 48px; 
                background-color: {}; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            "></div>''', obj.hex)
        return '-'

    list_display = ('color_preview', 'name', 'lvl', 'ral', 'mid_color', 'hex',)
    readonly_fields = ('color_preview',)
    inlines = [PaletteColorInline]
    search_fields=['name', 'ral']


class MaterialInline(admin.TabularInline):
    _obj = None
    model = Material

    def get_extra(self, request, obj=None, **kwargs):
        self._obj = obj
        return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'sub_group' and self._obj:
            kwargs["queryset"] = MaterialSubGroup.objects.filter(group=self._obj)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MaterialSubGroup)
class MaterialSubGroupAdmin(admin.ModelAdmin):
    inlines = [MaterialInline]


class MaterialSubGroupInline(admin.TabularInline):
    model = MaterialSubGroup
    extra = 0


@admin.register(MaterialGroups)
class MaterialGroupsAdmin(admin.ModelAdmin):
    inlines = [MaterialSubGroupInline, MaterialInline]

    def get_inline_instances(self, request, obj=None):
        instances = super().get_inline_instances(request, obj)

        if obj and obj.type == 'color':
            return []
        return instances
