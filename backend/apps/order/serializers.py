from rest_framework import serializers

from apps.order.models import Order, OrderProduct, OrderProductOptions, OrderNewPostDelivery
from drf_writable_nested.serializers import WritableNestedModelSerializer
from apps.attribute.serializers import AttributeSerializer


class OrderProductOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductOptions
        fields = ('option',)


class OrderProductSerializer(WritableNestedModelSerializer):
    options = OrderProductOptionsSerializer(many=True)

    class Meta:
        model = OrderProduct
        fields = ('product', 'sku', 'quantity', 'price', 'options',)
        read_only_fields = ('price',)


class OrderNewPostDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderNewPostDelivery
        fields = ('department',)


class OrderSerializer(WritableNestedModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'father_name', 'phone', 'email', 'created_at', 'delivery_type', 'products',
                  'newpost',)
        read_only_fields = ('created_at',)


class AdminOrderProductOptionsSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(source='option.value_attribute', read_only=True)
    group = serializers.CharField(source='option.attribute_group.attribute_group.name')

    class Meta:
        model = OrderProductOptions
        fields = ('group', 'attribute')
