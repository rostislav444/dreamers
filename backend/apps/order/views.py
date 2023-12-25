from rest_framework import viewsets, mixins, generics

from apps.order.models import Order
from apps.order.serializers import OrderSerializer
import json

class OrderViewSet(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.ViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()

    def create(self, request, *args, **kwargs):
        prety = json.dumps(request.data, indent=2)
        print(prety)
        data = super(OrderViewSet, self).create(request, *args, **kwargs)
        return data



