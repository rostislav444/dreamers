from rest_framework import serializers
from apps.attribute.models import PredefinedAttributeGroups


class PredefinedAttributeGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedAttributeGroups
        fields = ['id', 'name', 'type', 'group']
