from rest_framework import routers

from apps.catalogue import views

app_name = "catalogue"

router = routers.DefaultRouter()
router.register(r'products', views.CatalogueProductViewSet, basename="products")

urlpatterns = [] + router.urls
