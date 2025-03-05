from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.product.models import Sku
from apps.product.serializers.serializers_merchant import GoogleMerchantSkuSerializer


class GoogleMerchantFeedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для создания фида Google Merchant
    """
    queryset = Sku.objects.filter(images__isnull=False).distinct()
    serializer_class = GoogleMerchantSkuSerializer
    
    @action(detail=False, methods=['get'], renderer_classes=[TemplateHTMLRenderer])
    def xml(self, request):
        """
        Генерирует XML-фид для Google Merchant
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
            {'products': serializer.data},
            template_name='product/google_merchant_feed.xml'
        )
    
    @action(detail=False, methods=['get'])
    def json(self, request):
        """
        Генерирует JSON-фид для Google Merchant
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({'products': serializer.data}) 