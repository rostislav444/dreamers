from rest_framework import viewsets, mixins, generics

from apps.material.serializers import ColorSerializer
from apps.material.models import Color


class ColorsView(generics.GenericAPIView, mixins.ListModelMixin, viewsets.ViewSet):
    serializer_class = ColorSerializer

    def get_queryset(self):
        return Color.objects.all()
