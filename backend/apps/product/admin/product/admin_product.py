from django.contrib import admin

from apps.abstract.admin import ParentLinkMixin
from apps.product.forms import ProductOptionPriceMultiplierFromSet, ProductOptionPriceMultiplierFrom
from apps.product.models import Product, ProductOptionPriceMultiplier, ProductClass
from .admin_3d import Product3DBlenderModelInline
from .admin_product_attribute import ProductAttributeInline
from .admin_product_custom_parts import ProductCustomizedPartInline
from .admin_sku import SkuInline


# TODO add From, Formset, min and max
class ProductOptionPriceMultiplierInline(admin.StackedInline):
    model = ProductOptionPriceMultiplier
    form = ProductOptionPriceMultiplierFrom
    formset = ProductOptionPriceMultiplierFromSet

    @staticmethod
    def calc_num(obj):
        if not obj:
            return 0
        return obj.get_price_sub_group_multiplier_attribute_groups.count()

    def get_min_num(self, request, obj=None, **kwargs):
        return self.calc_num(obj)

    def get_max_num(self, request, obj=None, **kwargs):
        return self.calc_num(obj)



@admin.register(Product)
class ProductAdmin(ParentLinkMixin, admin.ModelAdmin):
    parent_model = ProductClass
    inlines = [
        ProductCustomizedPartInline,
        Product3DBlenderModelInline,
        ProductOptionPriceMultiplierInline,
        ProductAttributeInline,
        SkuInline
    ]
    fieldsets = [
        [None, {
            'fields': (
                'code', ('price', 'stock'),  'generate_sku_from_materials', 'remove_images'
            )
        }, ],
    ]
