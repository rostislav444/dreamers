from django.contrib import admin
from apps.attribute.abstract.admin import AttributeFildSet
from apps.attribute.models import AttributeGroup, Attribute
from apps.product.models import ProductClass, Product, ProductClassOptionGroup, ProductClassOption, \
    ProductClassProductAttributes
from apps.product.forms import ProductClassOptionGroupForm


class ProductClassProductAttributesInline(admin.TabularInline):
    model = ProductClassProductAttributes
    extra = 0


# Product Class Option
class ProductClassOptionInline(AttributeFildSet):
    model = ProductClassOption
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "value_attribute":
            parent_id = request.resolver_match.kwargs.get('object_id')
            kwargs["queryset"] = Attribute.objects.filter(group__product_class_option_group=parent_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Product Class Option Group
class ProductClassOptionGroupAbstract:
    form = ProductClassOptionGroupForm
    fieldsets = (
        (None, {
            'fields': ('name', ('type', 'attribute_group', 'unit', 'image_dependency'), 'save_all_options')
        },),
    )

    class Meta:
        abstract = True


@admin.register(ProductClassOptionGroup)
class ProductClassOptionGroupAdmin(ProductClassOptionGroupAbstract, admin.ModelAdmin):
    inlines = [ProductClassOptionInline]

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        for inline in super(ProductClassOptionGroupAdmin, self).get_inline_instances(request, obj):
            if inline.model.__name__ == ProductClassOption.__name__:
                if not obj.attribute_group or obj.attribute_group and not obj.attribute_group.custom:
                    inline_instances.append(inline)
        return obj and inline_instances or []


class ProductClassOptionGroupInline(ProductClassOptionGroupAbstract, admin.StackedInline):
    model = ProductClassOptionGroup
    show_change_link = True
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'attribute_group':
            parent_id = request.resolver_match.kwargs.get('object_id')
            try:
                product_class = self.parent_model.objects.get(id=parent_id)
                kwargs['queryset'] = product_class.possible_option_groups
            except self.parent_model.DoesNotExist:
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
        ProductClassOptionGroupInline,
        ProductClassProductAttributesInline,
        ProductInline
    ]



