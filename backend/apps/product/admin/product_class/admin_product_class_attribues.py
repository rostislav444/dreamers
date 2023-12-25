from apps.product.abstract.admin import FilterAttributeGroupsFK
from apps.product.forms import ProductClassAttributesForm
from apps.product.models import ProductClassAttributes


class ProductClassAttributesInline(FilterAttributeGroupsFK):
    model = ProductClassAttributes
    form = ProductClassAttributesForm
    extra = 0

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ProductClassAttributesInline, self).get_fieldsets(request, obj)
        # Set default field, that should be selected, until other appears
        fieldsets[0][1]['fields'] = ('attribute_group',)
        if obj:
            # Search for inline object
            item = self.model.objects.filter(product_class=obj).first()
            if item and item.attribute_group:
                if item.attribute_group.custom:
                    fieldsets[0][1]['fields'] = ('attribute_group', *item.attribute_group.actual_field_name)
                else:
                    fieldsets[0][1]['fields'] = ('attribute_group', 'value_attribute')

        return fieldsets

