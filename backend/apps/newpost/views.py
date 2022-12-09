from rest_framework import viewsets, mixins, generics

from apps.newpost.models import NewPostAreas, NewPostCities, NewPostDepartments
from apps.newpost.serializer import NewPostAreasSerializer, NewPostCitiesSerializer, NewPostDepartmentsSerializer


class NewPostAreasViewSet(generics.GenericAPIView, mixins.ListModelMixin, viewsets.ViewSet):
    serializer_class = NewPostAreasSerializer

    def get_queryset(self):
        return NewPostAreas.objects.all()


class NewPostCitiesViewSet(generics.GenericAPIView, mixins.ListModelMixin, viewsets.ViewSet):
    serializer_class = NewPostCitiesSerializer

    def get_queryset(self):
        area = self.request.GET.get('area')
        if self.request.GET.get('all'):
            qs = NewPostCities.objects.all()
        else:
            qs = NewPostCities.objects.filter(departments__isnull=False).distinct()
        if area:
            return qs.filter(region__area__ref=area)
        return qs


class NewPostDepartmentsViewSet(generics.GenericAPIView, mixins.ListModelMixin, viewsets.ViewSet):
    serializer_class = NewPostDepartmentsSerializer

    def get_queryset(self):
        city = self.request.GET.get('city')
        if city:
            return NewPostDepartments.objects.filter(city__ref=city)
        return NewPostDepartments.objects.all()
