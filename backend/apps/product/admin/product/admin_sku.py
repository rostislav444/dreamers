from django.contrib import admin
from django.utils.html import mark_safe

from apps.product.models import Sku, SkuOptions, SkuImages


class SkuImagesInline(admin.TabularInline):
    model = SkuImages
    extra = 0

    def image_tag(self, instance):
        path = instance.image.name
        if path:
            return mark_safe(f'''
                    <img src="/media/{path}" width="80" height="80" style="
                        border: 1px solid #ccc; border-radius: 6px; margin-top: -4px; object-fit: cover
                    " />
               ''')
        return None

    fields = ('index', 'image_tag', 'image',)
    readonly_fields = ('image_tag',)
    image_tag.short_description = 'Image preview'


class SkuOptionsInline(admin.TabularInline):
    model = SkuOptions
    extra = 0


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    inlines = [
        SkuOptionsInline,
        SkuImagesInline
    ]


class SkuInline(admin.TabularInline):
    show_change_link = True
    model = Sku
    extra = 0

    def name(self, object):
        return object.__str__()

    fields = ('name', 'code', 'quantity',)
    readonly_fields = ('name',)
