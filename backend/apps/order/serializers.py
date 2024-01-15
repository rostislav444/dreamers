from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.order.models import Order, OrderItem


class OrderItemSerializer(WritableNestedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('sku', 'quantity', 'price',)


class OrderSerializer(WritableNestedModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'father_name', 'phone', 'email', 'address', 'items')
