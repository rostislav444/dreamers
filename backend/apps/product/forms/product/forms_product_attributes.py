from django import forms

from apps.product.models import ProductAttribute


class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['attribute']

    def __init__(self, *args, group=None, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)
        if group:
            self.fields['attribute'].queryset = self.fields['attribute'].queryset.filter(attribute_group=group)
            self.fields['attribute'].label = group.attribute_group.name
            self.fields['attribute'].required = True


class ProductAttributeFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        # self.groups = self.instance.product_class.product_attributes_groups.all()
        super(ProductAttributeFormSet, self).__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        try:
            group = list(self.instance.product_class.product_attributes_groups.all())[index]
            kwargs['group'] = group
            return kwargs
        except (IndexError, TypeError):
            return kwargs
