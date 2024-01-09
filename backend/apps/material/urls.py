from rest_framework import routers

from apps.material import views

app_name = "material"

router = routers.DefaultRouter()
router.register(r'colors', views.ColorsView, basename="sku_images")

urlpatterns = [] + router.urls
