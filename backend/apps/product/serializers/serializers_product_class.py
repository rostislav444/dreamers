from rest_framework import serializers
from apps.product.models import ProductClassAttributes, ProductClassOptionGroup, ProductClassOption, ProductClass
from apps.product.serializers import ProductSerializer
from project.settings import MEDIA_URL


class ProductClassAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductClassAttributes
        fields = ['id']


class ProductClassOptionSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = ProductClassOption
        fields = ['id', 'value']

    def get_value(self, obj):
        value = obj.value
        image = value.get('image')
        if value.get('image'):
            request = self.context.get('request', None)
            if request is not None:
                value['image'] = request.build_absolute_uri(MEDIA_URL+image)
        return value


class ProductClassOptionGroupSerializer(serializers.ModelSerializer):
    options = ProductClassOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ProductClassOptionGroup
        fields = ['id', 'name', 'slug', 'options', 'image_dependency']


class ProductClassSerializer(serializers.ModelSerializer):
    attributes = ProductClassAttributesSerializer(many=True)
    option_groups = ProductClassOptionGroupSerializer(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = ProductClass
        fields = ['id', 'name', 'slug', 'attributes', 'option_groups', 'products']
