from django import forms
from apps.attribute.models import AttributeGroup
from apps.attribute.serializers import AttributeGroupSerializer
from apps.product.models import ProductAttribute


class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)

        fields = [field for field in self.fields]
        non_hidden_fields = ['group']

        data = kwargs.get('initial', None)
        if kwargs.get('instance', None):
            instance = kwargs['instance']
            data = AttributeGroupSerializer(instance.group).data

        if data:
            self.fields['group'].queryset = self.fields['group'].queryset.filter(id=data['pk'])
            self.fields['group'].empty_label = None
            if data['custom']:
                actual_field_name = data['actual_field_name']
                if type(actual_field_name) == list:
                    non_hidden_fields += actual_field_name
                else:
                    non_hidden_fields.append(actual_field_name)
            else:
                non_hidden_fields.append('value_attribute')

        for field in list(set(fields) - set(non_hidden_fields)):
            self.fields[field].widget = forms.HiddenInput()

    def save(self, commit=True):
        actual_field_name = self.instance.group.actual_field_name
        if type(actual_field_name) != list:
            actual_field_name = [actual_field_name]
        for field in actual_field_name:
            if getattr(self.instance, field):
                self.instance.save()
                break
        return self.instance


class ProductAttributeFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        if kwargs['instance'].pk:
            product = kwargs['instance']
            product_class = product.product_class
            attribute_groups_id = product.product_class.product_attributes.all().values_list('attribute_group', flat=True)
            possible_attribute_groups = product_class.possible_attribute_groups.filter(id__in=attribute_groups_id)
            kwargs.update({
                'initial': [AttributeGroupSerializer(group).data for group in possible_attribute_groups],
            })
        super(ProductAttributeFormSet, self).__init__(*args, **kwargs)
