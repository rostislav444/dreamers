from django.contrib import admin

from apps.product.models import ProductClass, Product
from .admin_product_class_attribues import ProductClassAttributesInline
from .admin_product_class_materials import ProductPartInline, ProductStaticPartInline
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
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'description', )
        }),
        ('Price', {
            'fields': (('initial_price', 'square_decimeter_price'),)
        }),
        ('Width', {
            'fields': (('min_width', 'max_width', 'width_step',),)
        }),
        ('Height', {
            'fields': (('min_height', 'max_height', 'height_step',),)
        }),
        ('Depth', {
            'fields': (('min_depth', 'max_depth', 'depth_step',),)
        }),
        ('Options', {
            'fields': (
                ('generate_sku_from_options', 'generate_variants_from_sizes'),
                ('generate_products_from_dimensions',),
            )
        }),
    )

    inlines = [
        ProductStaticPartInline,
        ProductPartInline,
        ProductClassAttributesInline,
        ProductClassOptionGroupInline,
        ProductClassOptionGroupCustomInline,
        ProductClassProductAttributeGroupsInline,
        ProductInline
    ]
