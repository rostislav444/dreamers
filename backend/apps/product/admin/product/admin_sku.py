from django.contrib import admin
from django.utils.html import mark_safe
from django_admin_inline_paginator.admin import TabularInlinePaginated

from apps.abstract.admin import ParentLinkMixin
from apps.product.models import Product, Sku, SkuImages
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

@admin.register(Sku)
class SkuAdmin(ParentLinkMixin, admin.ModelAdmin):
    parent_model = Product
    inlines = [
        SkuImagesInline
    ]

    def get_model_perms(self, request):
        return {}


class SkuInline(TabularInlinePaginated):
    show_change_link = True
    model = Sku
    extra = 0
