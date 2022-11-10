from django.contrib import admin
from apps.product.abstract.admin import ReturnToProductClassAdmin
from apps.product.models import Product, Product3DBlenderModel
from .admin_product_attribute import ProductAttributeInline
from .admin_sku import SkuInline


class Product3DBlenderModelInline(admin.StackedInline):
    model = Product3DBlenderModel


@admin.register(Product)
class ProductAdmin(ReturnToProductClassAdmin, admin.ModelAdmin):
    inlines = [
        Product3DBlenderModelInline,
        ProductAttributeInline,
        SkuInline
    ]

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                'fields': (
                    'product_class_link',
                    'code', ('price', 'stock'), ('render_variants', 'generate_sku'),
                )
            },),
        )


