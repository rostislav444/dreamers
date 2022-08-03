from django import forms
from apps.attribute.models import AttributeGroup
from apps.product.models import ProductAttribute


class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)

        if kwargs.get('initial', None):
            initial = kwargs['initial']
            self.fields['attribute_group'].queryset = self.fields['attribute_group'].queryset.filter(
                id=initial['attribute_group'])
            self.fields['attribute'].queryset = self.fields['attribute'].queryset.filter(
                group=initial['attribute_group'])
            self.fields['attribute'].required = initial['required']
        elif kwargs.get('instance', None):
            instance = kwargs['instance']
            self.fields['attribute_group'].queryset = self.fields['attribute_group'].queryset.filter(
                id=instance.attribute_group_id)
            self.fields['attribute'].queryset = self.fields['attribute'].queryset.filter(
                group=instance.attribute_group_id)
            self.fields['attribute'].required = instance.attribute_group.required == AttributeGroup.ATTRIBUTE


class ProductAttributeFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        if kwargs['instance'].pk:
            product = kwargs['instance']
            attribute_groups = product.get_required_attributes.exclude(
                pk__in=product.attributes.all().values_list('attribute_group', flat=True)
            )

            # .exclude(
            # required=AttributeGroup.OPTION, pk__in=product.attributes.all().values_list('attribute_group', flat=True))

            kwargs.update({
                'initial': [{
                        'attribute_group': attribute_group.pk,
                        'required': attribute_group.required,
                        'name': attribute_group.name
                    } for attribute_group in attribute_groups
                ],
            })
        super(ProductAttributeFormSet, self).__init__(*args, **kwargs)
