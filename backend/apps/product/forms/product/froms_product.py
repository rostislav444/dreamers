from django import forms

from apps.product.models import ProductOptionPriceMultiplier, ProductPartSceneMaterialImage


class ProductOptionPriceMultiplierFrom(forms.ModelForm):
    class Meta:
        model = ProductOptionPriceMultiplier
        fields = '__all__'

    def get_option_group_id(self, kwargs):
        option_group_id = None
        initial_data = kwargs.get('initial')
        if initial_data:
            option_group_id = initial_data.get('option_group')
        if self.instance and hasattr(self.instance, 'option_group'):
            option_group_id = self.instance.option_group.id
        return option_group_id

    def __init__(self, *args, **kwargs):
        super(ProductOptionPriceMultiplierFrom, self).__init__(*args, **kwargs)
        option_group_id = self.get_option_group_id(kwargs)

        if kwargs.get('initial') or self.instance:
            self.fields['option_group'].queryset = self.fields['option_group'].queryset.filter(id=option_group_id)
            self.fields['option_group'].empty_label = None


class ProductOptionPriceMultiplierFromSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            sub_group_multipliers = instance.get_price_sub_group_multiplier_attribute_groups
            kwargs.update({
                'initial': [{'option_group': multiplier.id} for multiplier in sub_group_multipliers],
            })
        super(ProductOptionPriceMultiplierFromSet, self).__init__(*args, **kwargs)


class ProductPartSceneMaterialImageForm(forms.ModelForm):
    class Meta:
        model = ProductPartSceneMaterialImage
        fields = ['image']