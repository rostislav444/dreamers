from django import forms

from apps.product.forms import ProductAttributeFormAbstract
from apps.product.models import ProductClassProductAttributes
from apps.attribute.serializers import AttributeGroupOnlySerializer


class ProductClassProductAttributesForm(ProductAttributeFormAbstract):
    class Meta:
        model = ProductClassProductAttributes
        fields = '__all__'


class ProductClassProductAttributesFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        if kwargs['instance'].pk:
            instance = kwargs['instance']
            kwargs.update({
                'initial': AttributeGroupOnlySerializer(instance.attribute_group).data,
            })
        super(ProductClassProductAttributesFormSet, self).__init__(*args, **kwargs)
