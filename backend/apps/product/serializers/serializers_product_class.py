from rest_framework import serializers

from apps.attribute.serializers import AttributeGroupOnlySerializer, AttributeSerializer, AttributeSubGroupSerializer
from apps.product.models import ProductClassAttributes, ProductClassOptionGroup, ProductClassOption, \
    ProductClassProductAttributeGroups, ProductClassProductAttributes, ProductClass
from apps.product.serializers import ProductSerializer
from project.settings import MEDIA_URL


class ProductClassAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductClassAttributes
        fields = ['id']


class ProductClassOptionSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    price = serializers.IntegerField(source='value_attribute.price')

    class Meta:
        model = ProductClassOption
        fields = ['id', 'value', 'price']

    def get_value(self, obj):
        value = obj.value
        image = value.get('image')
        if value.get('image'):
            request = self.context.get('request', None)
            if request is not None:
                value['image'] = request.build_absolute_uri(MEDIA_URL + image)
        return value


class ProductClassOptionGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_name')
    options = serializers.SerializerMethodField()
    sub_groups = serializers.SerializerMethodField()
    price_required = serializers.CharField(source='attribute_group.price_required'  , read_only=True)

    class Meta:
        model = ProductClassOptionGroup
        fields = ['id', 'name', 'slug', 'options', 'sub_groups', 'price_required', 'image_dependency']

    def get_sub_groups(self, instance):
        sub_groups = instance.attribute_group.sub_groups.all()
        if sub_groups.count() > 0:
            data = []
            for sub_group in sub_groups:
                options = ProductClassOptionSerializer(instance.options.filter(value_attribute__sub_group=sub_group),
                                                       many=True)
                options.context.update({'request': self.context.get('request', None)})
                serialized = AttributeSubGroupSerializer(sub_group).data
                serialized['options'] = options.data
                data.append(serialized)
            return data
        return 'options'

    def get_options(self, instance):
        if instance.attribute_group.sub_groups.count() == 0:
            options = ProductClassOptionSerializer(instance.options.all(), many=True)
            options.context.update({'request': self.context.get('request', None)})
            return options.data
        return 'sub_group'


class ProductClassProductAttributesSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)

    class Meta:
        model = ProductClassProductAttributes
        fields = ['id', 'attribute']


class ProductClassProductAttributeGroupsSerializer(serializers.ModelSerializer):
    attribute_group = AttributeGroupOnlySerializer(read_only=True)
    attributes = ProductClassProductAttributesSerializer(read_only=True, many=True)

    class Meta:
        model = ProductClassProductAttributeGroups
        fields = ['id', 'attribute_group', 'attributes']


class ProductClassSerializer(serializers.ModelSerializer):
    attributes = ProductClassAttributesSerializer(many=True)
    option_groups = ProductClassOptionGroupSerializer(many=True)
    product_attributes_groups = ProductClassProductAttributeGroupsSerializer(read_only=True, many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = ProductClass
        fields = ['id', 'name', 'slug', 'attributes', 'option_groups', 'product_attributes_groups', 'products']
