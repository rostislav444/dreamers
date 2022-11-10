from rest_framework import serializers

from apps.product.models import Sku, SkuOptions, SkuImages
from collections import OrderedDict


class SkuOptionsSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    option_id = serializers.IntegerField(source='option.id')
    model_3d_name = serializers.CharField(source='option.attribute_group.model_3d_name')

    class Meta:
        model = SkuOptions
        fields = ['id', 'option_id', 'value', 'group', 'model_3d_name']

    def get_value(self, obj):
        return obj.option.value

    def get_group(self, obj):
        return obj.option.attribute_group.slug


class SkuImagesSerializer(serializers.ModelSerializer):
    sku = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Sku.objects.all())

    class Meta:
        model = SkuImages
        fields = ['sku', 'image']


class SkuSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    images = SkuImagesSerializer(read_only=True, many=True)

    class Meta:
        model = Sku
        fields = ['id', 'options', 'images']

    def get_options(self, obj):
        data = OrderedDict()
        for option in obj.options.all():
            data[option.option.attribute_group.slug] = SkuOptionsSerializer(option).data
        return data
