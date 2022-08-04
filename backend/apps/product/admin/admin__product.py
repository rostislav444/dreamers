from django.contrib import admin
from apps.attribute.models import AttributeGroup
from apps.product.models import Product, Sku, SkuOptions, ProductAttribute
from apps.product.forms import ProductAttributeFormSet, ProductAttributeForm


class SkuOptionsInline(admin.TabularInline):
    model = SkuOptions
    extra = 0


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    inlines = [SkuOptionsInline]


class SkuInline(admin.TabularInline):
    show_change_link = True
    model = Sku
    extra = 0


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    formset = ProductAttributeFormSet
    form = ProductAttributeForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'group', 'value_text', 'value_integer', 'value_boolean', 'value_float', 'value_color_name',
                'value_color_hex', 'value_color_image', 'value_image_name', 'value_image_image',
                ('value_min', 'value_max',), 'value_attribute')
        },),
    )

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0
        return obj.get_required_attributes.count()

    def get_min_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0
        return obj.get_required_attributes.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductAttributeInline,
        SkuInline
    ]
