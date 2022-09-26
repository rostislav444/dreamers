from rest_framework import serializers
from apps.attribute.models import AttributeGroup, Attribute


class AttributeSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = ('pk', 'value')

    def get_value(self, obj):
        return obj.value()


class AttributeGroupSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(read_only=True, many=True)

    class Meta:
        model = AttributeGroup
        fields = ('pk', 'name', 'slug', 'type', 'custom', 'actual_field_name','attributes')
