from rest_framework import serializers

from apps.category.models import Category


class NestedCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'children'
        ]

    def get_children(self, instance):
        children = instance.get_children()
        if children.count() > 0:
            return NestedCategorySerializer(children, many=True).data
        return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug',
        ]
