from django import forms 
from apps.product.models import ProductClassOptionGroup


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
            else:
                self.fields['attribute_group'].widget = forms.HiddenInput()
                self.fields['save_all_options'].widget = forms.HiddenInput()

        else:
            self.fields['unit'].widget = forms.HiddenInput()
            self.fields['save_all_options'].widget = forms.HiddenInput()
