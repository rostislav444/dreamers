from collections import OrderedDict

from rest_framework import serializers

from apps.product.models import Sku, Product, Product3DBlenderModel, ProductClass
from .serializers_materials import ProductPartSerializer
from .serializers_sku import SkuImagesSerializer, SkuOptionsSerializer


class ProductRender3DBlenderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product3DBlenderModel
        fields = ['blend', 'blend1', 'mtl', 'obj']


class ProductRenderWithSkuSerializer(serializers.ModelSerializer):
    parts = ProductPartSerializer(many=True, read_only=True)
    # model_3d = ProductRender3DBlenderModelSerializer(read_only=True)

    class Meta:
        model = ProductClass
        fields = ['id', 'parts']
