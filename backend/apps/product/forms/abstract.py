from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from apps.attribute.models import AttributeGroup, Attribute
from apps.product.models import ProductClassAttributes


# Abstract
class AttributeFieldsForm(forms.ModelForm):
    value_text = forms.CharField(label=_('Text'), required=False)
    value_integer = forms.IntegerField(label=_('Integer'), required=False)
    value_boolean = forms.BooleanField(label=_('Boolean'), required=False)
    value_float = forms.FloatField(label=_('Float'), required=False)
    value_color_name = forms.CharField(label=_('Color'), required=False)
    value_color_hex = forms.CharField(label=_('Color HEX'), max_length=7, required=False)
    value_color_image = forms.ImageField(label=_('Color image'), required=False)
    value_image_name = forms.CharField(label=_('Name'), required=False)
    value_image_image = forms.ImageField(label=_('Image'), required=False)
    value_min = forms.IntegerField(label=_('Min'), required=False)
    value_max = forms.IntegerField(label=_('Max'), required=False)

    class Meta:
        abstract = True

    def set_required_fields(self, fields):
        for field in fields:
            self.fields[field].required = True

    def set_non_required_fields(self, fields):
        for field in fields:
            self.fields[field].required = False

    def hide_fields(self, fields):
        for field in list(set(self.fields) - set(fields)):
            self.fields[field].widget = forms.HiddenInput()


class ProductAttributeFormAbstract(AttributeFieldsForm):
    def __init__(self, *args, **kwargs):
        super(ProductAttributeFormAbstract, self).__init__(*args, **kwargs)


        # non_hidden_fields = ['attribute_group']
        #
        # initial_data = kwargs.get('initial', None)
        # instance = kwargs.get('instance', None)
        #
        # if initial_data:
        #     self.fields['attribute_group'].empty_label = None
        #     self.fields['attribute_group'].queryset = self.fields['attribute_group'].queryset.filter(id=initial_data['pk'])
        #     if initial_data['custom']:
        #         non_hidden_fields = [*non_hidden_fields, *initial_data['actual_field_name']]
        #         self.fields['attribute_group'].empty_label = None
        #     else:
        #         non_hidden_fields.append('value_attribute')
        #         self.fields['value_attribute'].queryset = self.fields['value_attribute'].queryset \
        #             .filter(attribute_group__pk=initial_data['pk'])
        # elif instance:
        #     if instance.attribute_group.custom:
        #         for field in instance.attribute_group.actual_field_name:
        #             non_hidden_fields.append(field)
        #             if instance.value_attribute:
        #                 self.fields[field].initial = getattr(instance.value_attribute, field)
        #     else:
        #         non_hidden_fields.append('value_attribute')
        #         self.fields['value_attribute'].queryset = self.fields['value_attribute'].queryset \
        #             .filter(attribute_group=instance.attribute_group)

        # self.hide_fields(non_hidden_fields)

    def clean(self):
        if self.cleaned_data['DELETE']:
            return self.cleaned_data
        base_fields, actual_field_name = ['attribute_group'], []
        attribute_group = self.cleaned_data.get('attribute_group', None)
        if attribute_group:
            if attribute_group.custom:
                actual_field_name = attribute_group.actual_field_name
            else:
                actual_field_name.append('value_attribute')
        return {k: v for k, v in self.cleaned_data.items() if k in [*base_fields, *actual_field_name]}

    def check_empty(self):
        actual_field_name = self.cleaned_data['attribute_group'].actual_field_name
        if type(actual_field_name) == list:
            empty = True
            for field in self.cleaned_data['attribute_group'].actual_field_name:
                if self.cleaned_data[field]:
                    empty = False
                    break
            return empty
        return not self.cleaned_data['attribute_group']

    @staticmethod
    def delete_useless_attribute(self, attribute=None):
        if not attribute:
            return
        if attribute.manual and attribute.product_attributes.count() < 2:
            attribute.delete()

    def save(self, commit=True):
        data = self.cleaned_data
        attribute_group = data.get('attribute_group', None)
        # Get current attribute
        value_attribute_old = self.instance.value_attribute
        # To display attribute fields, first the attribute_group should be saved to object
        if self.instance.__class__ == ProductClassAttributes and not self.instance.pk:
            self.instance.attribute_group = attribute_group
            self.instance.save()
            return self.instance
        # Check if form is empty
        if attribute_group.custom:
            if self.check_empty():
                return self.instance
            try:
                attribute = Attribute.objects.get(**self.cleaned_data)
            except ObjectDoesNotExist:
                attribute = Attribute(**self.cleaned_data, manual=True)
                attribute.save()
            self.instance.value_attribute = attribute
            self.instance.save()
        else:
            attribute = self.instance.value_attribute
            if attribute:
                self.instance.save()
        # Check if attribute changed and maybe delete unused
        if value_attribute_old != attribute:
            self.delete_useless_attribute(value_attribute_old)
        return self.instance


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
