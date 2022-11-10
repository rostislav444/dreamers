from django import forms

from apps.attribute.abstract.fields import AttributeGroupTypeAbstractField, OptionGroupField
from apps.product.forms import FilterAttributeGroupAbstract
from apps.product.models import ProductClassOptionGroup


class ProductClassOptionGroupForm(FilterAttributeGroupAbstract):
    class Meta:
        model = ProductClassOptionGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductClassOptionGroupForm, self).__init__(*args, **kwargs)
        self.fields['type'].choices = OptionGroupField.ATTRIBUTE_CHOICES
        # self.fields['name'].widget = forms.HiddenInput()
        # self.fields['unit'].widget = forms.HiddenInput()
        #
        # if instance:
        #     if instance.type == 'attribute':
        #         self.fields['unit'].widget.attrs['readonly'] = True
        #         self.fields['name'].widget = forms.HiddenInput()
        #     else:
        #         self.fields['attribute_group'].widget = forms.HiddenInput()
        #         self.fields['save_all_options'].widget = forms.HiddenInput()
        #         self.fields['name'].required = True
        # else:
        #     self.fields['name'].widget.attrs['readonly'] = True
        #     self.fields['unit'].widget = forms.HiddenInput()
        #     self.fields['save_all_options'].widget = forms.HiddenInput()


class ProductClassOptionGroupFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        if kwargs['queryset']:
            kwargs['queryset'] = kwargs['queryset'].filter(type=OptionGroupField.ATTRIBUTE)
        super(ProductClassOptionGroupFormSet, self).__init__(*args, **kwargs)


class ProductClassOptionCustomGroupForm(forms.ModelForm):
    class Meta:
        model = ProductClassOptionGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductClassOptionCustomGroupForm, self).__init__(*args, **kwargs)
        self.fields['type'].choices = AttributeGroupTypeAbstractField.TYPE_CHOICES
        self.fields['name'].required = True


class ProductClassOptionCustomGroupFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        if kwargs['queryset']:
            kwargs['queryset'] = kwargs['queryset'].exclude(type=OptionGroupField.ATTRIBUTE)
        super(ProductClassOptionCustomGroupFormSet, self).__init__(*args, **kwargs)
