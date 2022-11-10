from collections import OrderedDict

from rest_framework import serializers

from apps.product.models import Sku, Product, Product3DBlenderModel
from .serializers_sku import SkuImagesSerializer, SkuOptionsSerializer


class ProductRender3DBlenderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product3DBlenderModel
        fields = ['blend', 'blend1', 'mtl', 'obj']


class SkuRenderSerializer(serializers.ModelSerializer):
    options = SkuOptionsSerializer(many=True)
    images = SkuImagesSerializer(read_only=True, many=True)

    class Meta:
        model = Sku
        fields = ['id', 'options', 'images']


class ProductRenderWithSkuSerializer(serializers.ModelSerializer):
    sku = SkuRenderSerializer(read_only=True, many=True)
    model_3d = ProductRender3DBlenderModelSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'model_3d']
