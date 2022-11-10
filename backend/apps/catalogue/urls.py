from django.urls import path, include
from rest_framework import routers
from apps.catalogue import views


app_name = "catalogue"


router = routers.DefaultRouter()
router.register(r'', views.CatalogueProductViewSet, basename="products")


urlpatterns = [] + router.urls
