from django import forms

from apps.attribute.abstract import AttributeGroupTypeField
from apps.attribute.models import Attribute

form_attribute_custom_fields = {
    AttributeGroupTypeField.TEXT: (
        ('value_text', forms.CharField(max_length=500, required=True),),
    ),
    AttributeGroupTypeField.INTEGER: (
        ('value_integer', forms.IntegerField(required=True, min_value=0),),
    ),
    AttributeGroupTypeField.BOOLEAN: (
        ('value_boolean', forms.CheckboxInput(),),
    ),
    AttributeGroupTypeField.FLOAT: (
        ('value_float', forms.FloatField(required=True, min_value=0),),
    ),
    AttributeGroupTypeField.COLOR: (
        ('value_color_name', forms.CharField(max_length=255, required=True),),
        ('value_color_hex', forms.CharField(max_length=7, required=True),),
        ('value_color_image', forms.FileInput(),),
    ),
    AttributeGroupTypeField.RANGE: (
        ('value_min', forms.FloatField(required=True, min_value=0),),
        ('value_max', forms.FloatField(required=True, min_value=0),),
    ),
    AttributeGroupTypeField.IMAGE: (
        ('value_image_name', forms.CharField(max_length=255, required=True),),
        ('value_image_image', forms.FileInput(),),
    )
}


class AttributeFormAbstract(forms.ModelForm):
    value_text = forms.CharField(max_length=500, required=False)
    value_integer = forms.IntegerField(required=False)
    value_float = forms.FloatField(required=False, min_value=0)
    value_color_name = forms.CharField(max_length=255, required=False)
    value_color_hex = forms.CharField(max_length=7, required=False)
    value_color_image = forms.FileInput()
    value_min = forms.FloatField(required=False, min_value=0)
    value_max = forms.FloatField(required=False, min_value=0)
    value_image_name = forms.CharField(max_length=255, required=False)
    value_image_image = forms.FileInput()

    class Meta:
        abstract = True
        fields = ('attribute_group',)

    def __init__(self, *args, **kwargs):
        super(AttributeFormAbstract, self).__init__(*args, **kwargs)

        if self.instance and hasattr(self.instance, 'attribute_group'):
            attribute_group = self.instance.attribute_group

            if attribute_group.custom:
                for field_name, field in form_attribute_custom_fields[attribute_group.type]:
                    self.fields[field_name] = field

                    if self.instance.value_attribute:
                        self.fields[field_name].initial = getattr(self.instance.value_attribute, field_name)
            else:
                self.fields['value_attribute'] = forms.ModelChoiceField(
                    queryset=attribute_group.attributes,
                    widget=forms.Select(attrs={'class': 'form-control'})
                )

    def clean(self):
        cleaned_data = super(AttributeFormAbstract, self).clean()
        if self.instance and hasattr(self.instance, 'attribute_group'):
            attribute_group = self.instance.attribute_group
            if attribute_group.custom:
                for field_name, field in form_attribute_custom_fields[attribute_group.type]:
                    if not cleaned_data.get(field_name):
                        raise forms.ValidationError(
                            f'Field {field_name} is required'
                        )
                    else:
                        attr = attribute_group.attributes.filter(**{field_name: cleaned_data.get(field_name)}).first()
                        if not attr:
                            attr = Attribute(attribute_group=attribute_group, **{field_name: cleaned_data.get(field_name)})
                            attr.save()
                        cleaned_data['value_attribute'] = attr

        return cleaned_data


class AttributeInlineForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'sub_group' in self.cleaned_data and 'attribute_group' not in self.cleaned_data:
            cleaned_data['attribute_group'] = cleaned_data['sub_group'].group
        return cleaned_data
