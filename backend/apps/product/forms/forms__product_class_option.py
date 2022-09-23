from django import forms
from django.core.exceptions import ValidationError
from apps.product.models import ProductClassOptionGroup
from apps.attribute.models import AttributeGroup

class ProductClassOptionGroupForm(forms.ModelForm):
    class Meta:
        model = ProductClassOptionGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductClassOptionGroupForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        if instance:
            if instance.type == 'attribute':
                self.fields['unit'].widget = forms.HiddenInput()
                self.fields['name'].widget = forms.HiddenInput()
            else:
                self.fields['attribute_group'].widget = forms.HiddenInput()
                self.fields['save_all_options'].widget = forms.HiddenInput()
                self.fields['name'].required = True
        else:
            self.fields['name'].widget = forms.HiddenInput()
            self.fields['unit'].widget = forms.HiddenInput()
            self.fields['save_all_options'].widget = forms.HiddenInput()




# class ProductClassOptionGroupFormSet(forms.BaseInlineFormSet):
#     def __init__(self, *args, **kwargs):
#         if kwargs['instance'].pk:
#             instance = kwargs['instance']
#             attribute_groups = instance.possible_option_groups
#
#             kwargs.update({
#                 'initial': [{'attribute_group': group.pk} for group in attribute_groups],
#             })
#         super(ProductClassOptionGroupFormSet, self).__init__(*args, **kwargs)