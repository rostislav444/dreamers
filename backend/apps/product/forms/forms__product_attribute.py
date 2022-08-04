from django import forms
from apps.attribute.models import AttributeGroup
from apps.attribute.serializers import PredefinedAttributeGroupsSerializer
from apps.product.models import ProductAttribute


class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)

        print(kwargs.get('initial', None))

        fields = [field for field in self.fields]
        non_hidden_fields = ['group', 'type']

        data = kwargs.get('initial', None)
        if kwargs.get('instance', None):
            instance = kwargs['instance']
            data = PredefinedAttributeGroupsSerializer(instance).data

        if data:
            print(data)
        # if all(data.values()):
        #     self.fields['group'].queryset = self.fields['group'].queryset.filter(id=data['pk'])
        #     self.fields['group'].empty_label = None
        #     if data['custom']:
        #         actual_field_name = data['actual_field_name']
        #         if type(actual_field_name) == list:
        #             non_hidden_fields += actual_field_name
        #         else:
        #             non_hidden_fields.append(actual_field_name)
        #
        for field in list(set(fields) - set(non_hidden_fields)):
            self.fields[field].widget = forms.HiddenInput()


class ProductAttributeFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        if kwargs['instance'].pk:
            product = kwargs['instance']
            groups = product.get_required_attributes
            # .exclude(
            #     pk__in=product.attributes.all().values_list('group', flat=True)
            # )

            kwargs.update({
                'initial': [PredefinedAttributeGroupsSerializer(group).data for group in groups],
            })
        super(ProductAttributeFormSet, self).__init__(*args, **kwargs)
