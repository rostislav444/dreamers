from django import forms
from django.core.exceptions import ValidationError

from apps.attribute.abstract.fields import AttributeGroupTypeAbstractField, OptionGroupField
from apps.attribute.models import AttributeGroup
from apps.attribute.serializers import AttributeGroupSerializer
from apps.product.models import ProductAttribute, ProductClassOptionGroup, ProductClassAttributes, \
    ProductClassProductAttributes


# Abstract
class ProductAttributeFormAbstract(forms.ModelForm):
    class Meta:
        abstract = True

    def get_data(self, kwargs):
        data = kwargs.get('initial', None)
        if kwargs.get('instance', None):
            instance = kwargs['instance']
            data = AttributeGroupSerializer(instance.attribute_group).data
        return data

    def prepare_form(self, kwargs):
        data = self.get_data(kwargs)

        fields = [field for field in self.fields]
        non_hidden_fields = ['attribute_group']

        if data:
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

    def __init__(self, *args, **kwargs):
        super(ProductAttributeFormAbstract, self).__init__(*args, **kwargs)
        self.prepare_form(kwargs)

    # TODO make validation later
    # def save(self, commit=True):
    #     actual_field_name = self.instance.attribute_group.actual_field_name
    #     if type(actual_field_name) != list:
    #         actual_field_name = [actual_field_name]
    #     for field in actual_field_name:
    #         if getattr(self.instance, field):
    #             self.instance.save()
    #             break
    #     return self.instance


class FilterAttributeGroupAbstract(forms.ModelForm):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(FilterAttributeGroupAbstract, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.attribute_group:
            attribute_group_ids = self.fields['attribute_group'].queryset.values_list('pk', flat=True)
            self.fields['attribute_group'].queryset = AttributeGroup.objects.filter(
                id__in=[instance.attribute_group.id, *attribute_group_ids])