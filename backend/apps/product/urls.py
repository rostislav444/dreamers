from django.urls import path, include
from rest_framework import routers
from apps.product import views


app_name = "product"


router = routers.DefaultRouter()
router.register(r'', views.ProductViewSet, basename="products")


urlpatterns = [] + router.urls