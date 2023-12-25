from rest_framework import routers
from apps.order import views

app_name = "order"

router = routers.DefaultRouter()
router.register(r'', views.OrderViewSet, basename="orders")

urlpatterns = router.urls
