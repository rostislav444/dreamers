from rest_framework import serializers
from apps.attribute.models import AttributeGroup, Attribute, AttributeSubGroup, AttributeColor
from apps.material.models import Color


class AttributeSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = ('id', 'value')

    def get_value(self, obj):
        return obj.value


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'slug', 'hex', 'rgb')


class AttributeColorsSerializer(serializers.ModelSerializer):
    color = ColorsSerializer(read_only=True)

    class Meta:
        model = AttributeColor
        fields = ('id', 'color')


class AttributeGroupSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(read_only=True, many=True)

    class Meta:
        model = AttributeGroup
        fields = ('id', 'name', 'slug', 'type', 'custom', 'actual_field_name', 'attributes')


class AttributeGroupLiteSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(read_only=True, many=True)
    colors = AttributeColorsSerializer(read_only=True, many=True)
    name = serializers.CharField(source='get_name')

    class Meta:
        model = AttributeGroup
        fields = ('id', 'name', 'slug', 'type', 'attributes', 'colors')


class AttributeGroupOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeGroup
        fields = ('id', 'name', 'slug', 'type', 'custom', 'actual_field_name')


class ProductAttributeSerializer(serializers.ModelSerializer):
    value = serializers.JSONField()

    class Meta:
        model = Attribute
        fields = ('id', 'value')


class ProductAttributeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeGroup
        fields = ('id', 'name', 'slug', 'type')


class AttributeSubGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeSubGroup
        fields = ['id', 'name', 'slug', 'price']

