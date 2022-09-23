from rest_framework import serializers
from apps.attribute.models import AttributeGroup


class AttributeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeGroup
        fields = ['pk', 'custom', 'actual_field_name']
