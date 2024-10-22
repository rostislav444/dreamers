from django.contrib import admin

from apps.abstract.admin import ParentLinkMixin
from apps.product.forms import ProductOptionPriceMultiplierFromSet, ProductOptionPriceMultiplierFrom
from apps.product.models import Product, ProductOptionPriceMultiplier, ProductClass, ProductCustomizedPart
from .admin_3d import Product3DBlenderModelInline
from .admin_product_attribute import ProductAttributeInline
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


class ProductCustomizedPart(admin.TabularInline):
    model = ProductCustomizedPart
    readonly_fields = ['part']

    def __init__(self, *args, **kwrgs):
        self.materials_set = None
        super().__init__(*args, **kwrgs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'part' and self.materials_set:
            kwargs['queryset'] = self.materials_set.parts.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def calc_num(self, obj):
        if not obj:
            return 0
        self.materials_set = obj.product_class.materials_set
        if self.materials_set:
            return self.materials_set.parts.count()
        return 0

    def get_min_num(self, request, obj=None, **kwargs):
        return self.calc_num(obj)

    def get_max_num(self, request, obj=None, **kwargs):
        return self.calc_num(obj)



@admin.register(Product)
class ProductAdmin(ParentLinkMixin, admin.ModelAdmin):
    parent_model = ProductClass
    inlines = [
        ProductCustomizedPart,
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
