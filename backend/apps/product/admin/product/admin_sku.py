from django.contrib import admin
from django.utils.html import mark_safe
from django_admin_inline_paginator.admin import TabularInlinePaginated

from apps.abstract.admin import ParentLinkMixin
from apps.product.models import Product, Sku, SkuOptions, SkuImages, SkuMaterials
from project.settings import MEDIA_URL


class SkuImagesInline(admin.TabularInline):
    model = SkuImages
    extra = 0

    def image_tag(self, instance):
        path = instance.image.name

        if path:
            print(MEDIA_URL, path)
            return mark_safe(f'''
                    <img src="{MEDIA_URL}{path}" width="120" height="80" style="
                        border: 1px solid #ccc; border-radius: 6px; margin-top: -4px; object-fit: cover
                    " />
               ''')
        return None

    fields = ('index', 'image_tag', 'image',)
    readonly_fields = ('image_tag', )
    image_tag.short_description = 'Image preview'


class SkuMaterialsInline(admin.TabularInline):
    model = SkuMaterials
    extra = 0


class SkuOptionsInline(admin.TabularInline):
    model = SkuOptions
    extra = 0


@admin.register(Sku)
class SkuAdmin(ParentLinkMixin, admin.ModelAdmin):
    parent_model = Product
    inlines = [
        SkuMaterialsInline,
        SkuOptionsInline,
        SkuImagesInline
    ]


class SkuInline(TabularInlinePaginated):
    show_change_link = True
    model = Sku
    extra = 0

    can_delete = True

    def name(self, object):
        data = []

        for material in object.materials.all():
            part = material.get_material_part_name
            material_name = material.material.get_value
            material_type = material.material.group_type
            li_str = f'<li><b>{part}</b> - <span>{material_name} {material_type[0]}</span></li>'
            data.append(li_str)

        return mark_safe(f'<ul>{"".join(data)}</ul>')

    fields = ('name', 'code', 'quantity',)
    readonly_fields = ('name',)
