from django.contrib import admin
from apps.attribute.abstract.admin import AttributeFildSet
from apps.attribute.models import AttributeGroup, Attribute
from apps.product.models import ProductClass, Product, ProductClassOptionGroup, ProductClassOption, \
    ProductClassProductAttributes, ProductClassAttributes
from apps.product.forms import ProductClassOptionGroupForm, ProductClassOptionCustomGroupForm, \
    ProductClassAttributesForm, ProductClassProductAttributesForm, ProductClassOptionCustomGroupFormSet, \
    ProductClassOptionGroupFormSet


def filter_attribute_groups(request):
    print('filter_attribute_groups')
    # Product class id from django-admin url
    product_class = ProductClass.objects.get(id=request.resolver_match.kwargs.get('object_id'))

    # Attribute groups that assigned to product class category and category ancestors
    attribute_groups = product_class.possible_attribute_groups

    # Get ids of already assign attributes to products class
    product_class_attributes_groups_ids = product_class.attributes.all().values_list('attribute_group', flat=True)
    product_attribute_groups_ids = product_class.product_attributes.all().values_list('attribute_group', flat=True)

    # Return queryset
    return attribute_groups.exclude(id__in=[*product_class_attributes_groups_ids, *product_attribute_groups_ids])


class FilterAttributeGroupsFK(admin.StackedInline):
    class Meta:
        abstract = True

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "attribute_group":
            kwargs["queryset"] = filter_attribute_groups(request)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductClassAttributesInline(FilterAttributeGroupsFK):
    model = ProductClassAttributes
    form = ProductClassAttributesForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'attribute_group', 'value_text', 'value_integer', 'value_boolean', 'value_float', 'value_color_name',
                'value_color_hex', 'value_color_image', 'value_image_name', 'value_image_image',
                ('value_min', 'value_max',))
        },),
    )


class ProductClassProductAttributesInline(admin.TabularInline, FilterAttributeGroupsFK):
    model = ProductClassProductAttributes
    form = ProductClassProductAttributesForm
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


@admin.register(ProductClassOptionGroup)
class ProductClassOptionGroupAdmin(admin.ModelAdmin):
    inlines = [ProductClassOptionInline]

    fieldsets = (
        (None, {
            'fields': ('type', 'name', ('attribute_group', 'unit'), 'save_all_options', 'image_dependency')
        },),
    )

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        for inline in super(ProductClassOptionGroupAdmin, self).get_inline_instances(request, obj):
            if inline.model.__name__ == ProductClassOption.__name__:
                if not obj.attribute_group or obj.attribute_group and not obj.attribute_group.custom:
                    inline_instances.append(inline)
        return obj and inline_instances or []


class ProductClassOptionGroupInline(admin.TabularInline, FilterAttributeGroupsFK):
    model = ProductClassOptionGroup
    form = ProductClassOptionGroupForm
    formset = ProductClassOptionGroupFormSet
    show_change_link = True
    extra = 0
    fields = ('type', 'attribute_group', 'image_dependency', 'save_all_options')


class ProductClassOptionGroupCustomInline(admin.TabularInline):
    model = ProductClassOptionGroup
    form = ProductClassOptionCustomGroupForm
    formset = ProductClassOptionCustomGroupFormSet
    show_change_link = True
    extra = 0
    fields = ('type', 'name', 'unit', 'image_dependency')


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
        ProductClassProductAttributesInline,
        ProductInline
    ]
