from django import forms

from apps.product.forms import ProductAttributeFormAbstract
from apps.product.models import ProductAttribute


class ProductAttributeForm(ProductAttributeFormAbstract):
    class Meta:
        model = ProductAttribute
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductAttributeForm, self).__init__(*args, **kwargs)


class ProductAttributeFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        # if kwargs['instance'].pk:
        #     product = kwargs['instance']
        #     kwargs.update({
        #         'initial': [AttributeGroupOnlySerializer(item.attribute_group).data for item in
        #                     product.product_class.product_attributes.all()],
        #     })
        super(ProductAttributeFormSet, self).__init__(*args, **kwargs)

