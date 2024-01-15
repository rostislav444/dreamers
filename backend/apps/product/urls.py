from django.urls import path
from rest_framework import routers

from apps.product import views

app_name = "product"

router = routers.DefaultRouter()

router.register(r'render', views.ProductClassRenderViewSet, basename="product_render")
router.register(r'product_class', views.ProductClassViewSet, basename="product_class")
router.register(r'product', views.ProductViewSet, basename="products")
router.register(r'load_sku_images', views.LoadSkuImageView, basename="sku_images")

urlpatterns = [
    path('products_list', views.products_list)
]

urlpatterns += router.urls
