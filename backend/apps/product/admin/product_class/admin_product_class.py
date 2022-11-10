from django.contrib import admin

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
    inlines = [
        ProductClassAttributesInline,
        ProductClassOptionGroupInline,
        ProductClassOptionGroupCustomInline,
        ProductClassProductAttributeGroupsInline,
        ProductInline
    ]
