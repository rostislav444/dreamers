from django import forms

from apps.attribute.models import Attribute
from apps.product.forms import AttributeFieldsForm
from apps.product.models import ProductClassProductAttributes


class ProductClassProductAttributesForm(AttributeFieldsForm):
    class Meta:
        model = ProductClassProductAttributes
        fields = '__all__'

    def set_initial_data(self, actual_field_name):
        if self.instance.id:
            for field in actual_field_name:
                self.fields[field].initial = getattr(self.instance.attribute, field)

    def __init__(self, *args, group, **kwargs):
        self.group = group
        super(ProductClassProductAttributesForm, self).__init__(*args, **kwargs)
        actual_field_name = group.attribute_group.actual_field_name
        self.hide_fields(['attribute_group', *actual_field_name])
        self.set_required_fields(actual_field_name)
        self.set_non_required_fields(['attribute'])
        self.set_initial_data(actual_field_name)

    def save(self, commit=True):
        attribute_group = self.group.attribute_group
        data = {'attribute_group': attribute_group}
        for field in attribute_group.actual_field_name:
            data[field] = self.cleaned_data.get(field)
        attribute, _ = Attribute.objects.get_or_create(**data)
        self.instance.attribute = attribute
        self.instance.save()
        return self.instance


class ProductClassProductAttributesFormSet(forms.BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['group'] = self.instance
        return kwargs
