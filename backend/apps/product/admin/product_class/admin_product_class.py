from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe

from apps.product.models import ProductClass, Product
from .admin_product_class_attribues import ProductClassAttributesInline
from .admin_product_class_options import ProductClassOptionGroupInline, ProductClassOptionGroupCustomInline
from .admin_product_class_product_attributes import ProductClassProductAttributeGroupsInline
from project.settings import MEDIA_URL


# Product
class ProductInline(admin.TabularInline):
    show_change_link = True
    model = Product
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0


# Product class
@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    def materials_set_link(self, obj):
        instance = obj.materials_set
        if not instance:
            return '-'
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label, instance._meta.model_name), args=[instance.id])
        return mark_safe('<a href="%s" target="_blank">Открыть</a>' % url)

    def parts_image(self, obj):
        images_style = {
            'position': 'absolute',
            'object-fit': 'cover',
            'width': '100%',
            'height': '100%',
            'top': 0,
        }
        images_style_inline = ''.join(['%s: %s;' % (key, value) for key, value in images_style.items()])

        # Container for all product variants
        all_variants_html = []

        # Get images for each product
        for product in obj.products.all():
            parts_images = product.get_parts_images
            if parts_images:
                images_html = ['<img src="%s%s" style="%s">' % (MEDIA_URL, image, images_style_inline)
                               for image in parts_images]

                variant_container = ''.join([
                    '<div style="position: relative; width: 160px; height: 160px;">',
                    *images_html,
                    '</div>'
                ])
                all_variants_html.append(variant_container)

        # Wrap all variants in a flex container for better layout
        return mark_safe(
            '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; min-height: 120px; min-width: 120px; background-color: rgba(255,255,255, 0.1): padding: 5px;">' +
            ''.join(all_variants_html) +
            '</div>'
        )

    parts_image.short_description = 'Изображение (из частей)'

    fieldsets = (
        (None, {
            'fields': (
                'category', 'collection', 'interior', ('materials_set', 'materials_set_link',),'number_in_collection', 'name', 'description',)
        }),
        ('Цена', {
            'fields': (('initial_price', 'square_decimeter_price'),)
        }),
        ('Ширина', {
            'fields': (('min_width', 'max_width', 'width_step',),)
        }),
        ('Высота', {
            'fields': (('min_height', 'max_height', 'height_step',),)
        }),
        ('Глубина', {
            'fields': (('min_depth', 'max_depth', 'depth_step',),)
        }),
        ('Опции', {
            'fields': (
                ('generate_sku_from_options', 'generate_variants_from_sizes'),
            )
        }),
    )

    list_display = ('parts_image', 'name', 'category', 'materials_set', 'initial_price',)
    readonly_fields = ('parts_image', 'materials_set_link',)

    inlines = [
        ProductClassAttributesInline,
        ProductClassOptionGroupInline,
        ProductClassOptionGroupCustomInline,
        ProductClassProductAttributeGroupsInline,
        ProductInline
    ]
