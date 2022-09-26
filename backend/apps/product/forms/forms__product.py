from django import forms

from apps.attribute.serializers import AttributeGroupSerializer
from apps.product.forms import ProductAttributeFormAbstract
from apps.product.models import ProductAttribute


# Product attribute
class ProductAttributeForm(ProductAttributeFormAbstract):
    class Meta:
        model = ProductAttribute
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)

        data = self.get_data(kwargs)
        if data:
            self.fields['attribute_group'].queryset = self.fields['attribute_group'].queryset.filter(id=data['pk'])
            self.fields['attribute_group'].empty_label = None
        print(data)


class ProductAttributeFormSet(forms.BaseInlineFormSet):
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
        super(ProductAttributeFormSet, self).__init__(*args, **kwargs)

