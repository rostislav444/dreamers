from admin_auto_filters.filters import AutocompleteFilter
from apps.material.models import (
    BaseColor,
    BlenderMaterial,
    Color,
    Manufacturer,
    Material,
    MaterialGroups,
    MaterialSubGroup,
    Palette,
    PaletteColor,
)
from apps.material.utils.blender_matrial_admin_preview import blender_material_preview
from django.contrib import admin
from django.utils.html import format_html
from django_admin_inline_paginator.admin import TabularInlinePaginated


class BlenderMaterialFilter(AutocompleteFilter):
    title = "Color"
    field_name = "color"


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(BlenderMaterial)
class BlenderMaterialAdmin(admin.ModelAdmin):
    search_fields = ["color__name"]
    autocomplete_fields = ["color"]
    readonly_fields = ("show_preview", "preview")

    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "name",
                    "copy_from",
                )
            },
        ),
        (
            "Preview",
            {
                "fields": (
                    "show_preview",
                    "preview",
                )
            },
        ),
        (
            "Base Maps",
            {
                "fields": (
                    ("col", "color"),
                    ("nrm_gl", "nrm_dx"),
                )
            },
        ),
        (
            "Detail Maps",
            {
                "fields": (
                    ("bump", "bump16"),
                    ("disp", "disp16"),
                )
            },
        ),
        (
            "Material Properties",
            {
                "fields": (
                    ("rgh", "rgh_num"),
                    ("mtl", "mtl_num"),
                    ("refl", "refl_num"),
                    ("ao", "ao_num"),
                )
            },
        ),
        (
            "Scaling",
            {
                "fields": (("scale", "aspect_ratio"),),
                "classes": ("collapse",),
                "description": "Настройки масштабирования текстур",
            },
        ),
    )

    @staticmethod
    def show_preview(obj):
        return blender_material_preview(obj)

    show_preview.short_description = "Color Preview"


@admin.register(BaseColor)
class BaseColorAdmin(admin.ModelAdmin):
    @staticmethod
    def color_preview(obj):
        if obj.hex:
            return format_html(
                """<div style="
                width: 48px; 
                height: 48px; 
                background-color: {}; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            "></div>""",
                obj.hex,
            )
        return "-"

    list_display = (
        "color_preview",
        "name",
        "lvl",
        "index",
        "hex",
    )
    readonly_fields = ("color_preview",)


class PaletteColorInline(admin.TabularInline):
    model = PaletteColor
    extra = 0


@admin.register(Palette)
class PaletteAdmin(admin.ModelAdmin):
    def colors(self, obj):
        data = []
        for hex_color in (
            obj.colors.all().order_by("color__ral").values_list("color__hex", flat=True)
        ):
            data.append(
                f'<div style="background-color: {hex_color}; width: 48px; height: 48px; margin: 2px;"></div>'
            )
        return format_html(
            '<div style="display: grid; grid-template-columns: repeat(auto-fill, 48px); gap: 4px;">'
            + "".join(data)
            + "</div>"
        )

    inlines = [PaletteColorInline]
    list_display = (
        "name",
        "colors",
    )
    readonly_fields = ("colors",)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    @staticmethod
    def color_preview(obj):
        if obj.hex:
            return format_html(
                """<div style="
                width: 48px; 
                height: 48px; 
                background-color: {}; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            "></div>""",
                obj.hex,
            )
        return "-"

    list_display = (
        "color_preview",
        "name",
        "lvl",
        "ral",
        "mid_color",
        "hex",
    )
    readonly_fields = ("color_preview",)
    inlines = [PaletteColorInline]
    search_fields = ["name", "ral"]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


class MaterialInline(TabularInlinePaginated):
    _obj = None
    model = Material
    show_change_link = True
    readonly_fields = ("preview",)
    autocomplete_fields = ["color"]
    search_fields = ["color__name"]
    per_page = 10

    def get_fieldsets(self, request, obj=None):
        custom_fieldsets = []

        if obj and obj.type == "color" and obj.color_only:
            return ((None, {"fields": ("preview", "color", "name", "sub_group")}),)
        if obj and obj.type == "color":
            custom_fieldsets.append("color")
        if obj and obj.type == "material":
            custom_fieldsets.extend(["image", "blender_material"])

        return (
            (None, {"fields": ("name", "sub_group")}),
            ("View", {"fields": ("preview", *custom_fieldsets)}),
            (
                "Manufacturer",
                {
                    "fields": (
                        "manufacturer",
                        "manufacturer_name",
                        "code",
                        "price",
                        "sheet_price",
                        "store_link",
                    )
                },
            ),
            ("Dimensions", {"fields": (("width", "height", "depth"),)}),
        )

    @staticmethod
    def preview(obj):
        if obj.group.type == "color" and obj.color:
            return format_html(
                '<div style="width: 48px; height: 48px; background-color: {};"></div>',
                obj.color.hex,
            )
        blender_material = obj.blender_material
        if blender_material:
            return blender_material_preview(blender_material)
        return "-"

    def get_extra(self, request, obj=None, **kwargs):
        self._obj = obj
        return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sub_group" and self._obj:
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

    # def get_inline_instances(self, request, obj=None):
    #     instances = super().get_inline_instances(request, obj)

    #     if obj and obj.type == "color":
    #         return []
    #     return instances
