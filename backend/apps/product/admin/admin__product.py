from django.contrib import admin
from apps.attribute.models import AttributeGroup
from apps.product.models import Product, Sku, SkuOptions, ProductAttribute
from apps.product.forms import ProductAttributeFormSet, ProductAttributeForm

from django.urls import reverse
from django.utils.safestring import mark_safe

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

    def name(self, object):
        return object.__str__()

    fields = ('name', 'code', 'quantity',)
    readonly_fields = ('name',)


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    formset = ProductAttributeFormSet
    form = ProductAttributeForm

    fieldsets = (
        (None, {
            'fields': (
                'group', 'value_text', 'value_integer', 'value_boolean', 'value_float', 'value_color_name',
                'value_color_hex', 'value_color_image', 'value_image_name', 'value_image_image',
                ('value_min', 'value_max',), 'value_attribute')
        },),
    )

    def get_max_num_count(self, obj):
        if not obj:
            return 0
        return obj.product_class.product_attributes.count()

    def get_max_num(self, request, obj=None, **kwargs):
        return self.get_max_num_count(obj)

    def get_extra(self, request, obj=None, **kwargs):
        return self.get_max_num_count(obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super(ProductAttributeInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductAttributeInline,
        # SkuInline
    ]

    @staticmethod
    def product_class_link(obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:product_productclass_change", args=(obj.product_class.pk,)),
            'Back to: ' + obj.product_class.__str__()
        ))

    fieldsets = (
        (None, {
            'fields': (
                'product_class_link',
                'code', ('price', 'stock'), 'model_3d', ('render_variants', 'generate_sku'),
            )
        },),
    )
    readonly_fields = ('product_class_link',)

