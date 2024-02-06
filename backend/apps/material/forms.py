from django import forms

from apps.material.models import ProductStaticPart


class ProductStaticPartForm(forms.ModelForm):
    class Meta:
        model = ProductStaticPart
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductStaticPartForm, self).__init__(*args, **kwargs)
        hide_fields = ['color', 'material']

        if self.instance and self.instance.pk and self.instance.group.type:
            hide_fields.remove(self.instance.group.type)

            if self.instance.group.type == 'material':
                self.fields['material'].queryset = self.instance.group.materials.all()

        for field in hide_fields:
            self.fields[field].widget = forms.HiddenInput()
