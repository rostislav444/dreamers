from django.contrib import admin
from apps.attribute.abstract.admin import AttributeFildSet
from apps.attribute.models import AttributeGroup, Attribute
from apps.product.models import ProductClass, Product, ProductClassProperty, ProductClassOptionGroup, \
    ProductClassOption
from apps.product.forms import ProductClassPropertyAdminFormSet, ProductClassPropertyInlineAdminFrom, \
    ProductClassOptionGroupForm


# Product Class Option
class ProductClassOptionInline(AttributeFildSet):
    model = ProductClassOption
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if obj:
            if obj.type == 'attribute' and not obj.attribute_group:
                return 0
        else:
            return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "value_attribute":
            parent_id = request.resolver_match.kwargs.get('object_id')
            kwargs["queryset"] = Attribute.objects.filter(group__product_class_option_group=parent_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ProductClassOptionGroup
class ProductClassOptionGroupAdminAbstract:
    form = ProductClassOptionGroupForm
    fieldsets = (
        (None, {
            'fields': ('name', ('type', 'attribute_group', 'unit'),'save_all_options',)
        },),
    )


@admin.register(ProductClassOptionGroup)
class ProductClassOptionGroupAdmin(ProductClassOptionGroupAdminAbstract, admin.ModelAdmin):
    inlines = [ProductClassOptionInline]


class ProductClassOptionGroupInline(ProductClassOptionGroupAdminAbstract, admin.StackedInline):
    model = ProductClassOptionGroup
    extra = 0
    show_change_link = True

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0


# Property
class ProductClassPropertyInline(admin.StackedInline):
    model = ProductClassProperty
    fields = (('property', 'name'),)
    formset = ProductClassPropertyAdminFormSet
    form = ProductClassPropertyInlineAdminFrom
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0


# Product
class ProductInline(admin.StackedInline):
    show_change_link = True
    model = Product
    extra = 0


# Product class
@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    inlines = [
        ProductClassPropertyInline,
        ProductClassOptionGroupInline,
        ProductInline
    ]



