from django.urls import path
from rest_framework import routers

from apps.product import views
from apps.product.views.views_merchant import GoogleMerchantFeedViewSet


app_name = "product"

router = routers.DefaultRouter()

router.register(r'render', views.ProductRenderViewSet, basename="product_render")
router.register(r'product_class', views.ProductClassViewSet, basename="product_class")
router.register(r'product', views.ProductViewSet, basename="products")
router.register(r'load_sku_images', views.LoadSkuImageView, basename="sku_images")
router.register(r'load_scene_material', views.LoadProductPartSceneMaterialImageView, basename="load_scene_material")
router.register(r'interior', views.RenderInteriorViewSet, basename="interior")
router.register(r'load_interior', views.LoadInteriorPartImageView, basename="load_interior")
router.register(r'merchant-feed', GoogleMerchantFeedViewSet)


urlpatterns = [
    path('products_list', views.products_list),
]

urlpatterns += router.urls
