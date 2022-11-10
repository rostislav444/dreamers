from django import forms

from apps.attribute.serializers import AttributeGroupSerializer
from apps.product.forms import ProductAttributeFormAbstract, FilterAttributeGroupAbstract
from apps.product.models import ProductClassAttributes, \
    ProductClassProductAttributeGroups


class ProductClassAttributesForm(ProductAttributeFormAbstract, FilterAttributeGroupAbstract):
    class Meta:
        model = ProductClassAttributes
        fields = '__all__'


class ProductClassAttributeFormSet(forms.BaseInlineFormSet):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        if kwargs['instance'].pk:
            product = kwargs['instance']
            product_class = product.product_class
            attribute_groups_id = product.product_class.product_attributes.all().values_list('attribute_group',
                                                                                             flat=True)
            possible_attribute_groups = product_class.possible_attribute_groups.filter(id__in=attribute_groups_id)
            kwargs.update({
                'initial': [AttributeGroupSerializer(attribute_group).data for attribute_group in
                            possible_attribute_groups],
            })
        super(ProductClassAttributeFormSet, self).__init__(*args, **kwargs)


class ProductClassProductAttributeGroupsForm(FilterAttributeGroupAbstract):
    class Meta:
        model = ProductClassProductAttributeGroups
        fields = '__all__'
