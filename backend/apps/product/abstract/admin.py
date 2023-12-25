import abc

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.product.models import ProductClass, Product, ProductAttribute


def filter_attribute_groups(request, model):
    methods_by_model_name = {
        'ProductClassAttributes': 'attr_groups_for_product_class_attributes',
        'ProductClassOptionGroup': 'attr_groups_for_product_class_options',
        'ProductClassProductAttributeGroups': 'attr_groups_for_product_class_product_attributes',
    }
    object_id = request.resolver_match.kwargs.get('object_id')
    if not object_id:
        return model.objects.none()
    product_class = ProductClass.objects.get(id=object_id)
    return getattr(product_class, methods_by_model_name[model.__name__])


class FilterAttributeGroupsFK(admin.StackedInline):
    class Meta:
        abstract = True

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "attribute_group":
            kwargs["queryset"] = filter_attribute_groups(request, self.model)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


