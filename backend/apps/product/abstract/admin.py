import abc

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.product.models import ProductClass, Product, ProductAttribute


def filter_attribute_groups(request, model):
    # Product class id from django-admin url
    object_id = request.resolver_match.kwargs.get('object_id')
    if not object_id:
        return model.objects.none()

    if model == ProductAttribute:
        product = Product.objects.get(id=object_id)
        product_class = product.product_class
    else:
        product_class = ProductClass.objects.get(id=object_id)

    # Attribute groups that assigned to product class category and category ancestors
    attribute_groups = product_class.possible_attribute_groups
    return attribute_groups
    # # Get ids of already assign attributes to products class
    # product_class_attributes_groups_ids = product_class.attributes.all().values_list('attribute_group', flat=True)
    # product_attribute_groups_ids = product_class.product_attributes.all().values_list('attribute_group', flat=True)
    #
    #
    # # Return queryset
    # return attribute_groups.exclude(id__in=[*product_class_attributes_groups_ids, *product_attribute_groups_ids])


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


class ReturnToProductClassAdmin:
    class Meta:
        abstract = True

    @staticmethod
    def product_class_link(obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:product_productclass_change", args=(obj.product_class.pk,)),
            'Back to: ' + obj.product_class.__str__()
        ))

    readonly_fields = ('product_class_link',)

    @abc.abstractmethod
    def get_fieldsets(self, request, obj=None):
        pass
