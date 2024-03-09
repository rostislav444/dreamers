from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe
from apps.product.models import ProductClass, Product
from .admin_product_class_attribues import ProductClassAttributesInline
from .admin_product_class_options import ProductClassOptionGroupInline, ProductClassOptionGroupCustomInline
from .admin_product_class_product_attributes import ProductClassProductAttributeGroupsInline


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

    fieldsets = (
        (None, {
            'fields': ('category', 'collection', ('materials_set', 'materials_set_link',), 'name', 'description',)
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

    readonly_fields = ['materials_set_link']

    inlines = [
        ProductClassAttributesInline,
        ProductClassOptionGroupInline,
        ProductClassOptionGroupCustomInline,
        ProductClassProductAttributeGroupsInline,
        ProductInline
    ]
