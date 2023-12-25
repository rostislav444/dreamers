from apps.attribute.forms import AttributeFormAbstract
from apps.product.forms import FilterAttributeGroupAbstract
from apps.product.models import ProductClassAttributes, \
    ProductClassProductAttributeGroups


class ProductClassAttributesForm(AttributeFormAbstract):
    class Meta:
        model = ProductClassAttributes
        fields = AttributeFormAbstract.Meta.fields


class ProductClassProductAttributeGroupsForm(FilterAttributeGroupAbstract):
    class Meta:
        model = ProductClassProductAttributeGroups
        fields = '__all__'
