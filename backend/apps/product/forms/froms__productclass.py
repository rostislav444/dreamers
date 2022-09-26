from django import forms
from django.core.exceptions import ValidationError

from apps.attribute.abstract.fields import AttributeGroupTypeAbstractField, OptionGroupField
from apps.attribute.serializers import AttributeGroupSerializer
from apps.product.forms import ProductAttributeFormAbstract, FilterAttributeGroupAbstract
from apps.product.models import ProductAttribute, ProductClassOptionGroup, ProductClassAttributes, \
    ProductClassProductAttributes


# TODO Add "value_attribute" field
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


class ProductClassProductAttributesForm(FilterAttributeGroupAbstract):
    class Meta:
        model = ProductClassProductAttributes
        fields = '__all__'


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