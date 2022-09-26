from rest_framework import routers
from apps.attribute import views

app_name = "attribute"

router = routers.DefaultRouter()
router.register(r'', views.AttributesViewSet, basename="attributes")

urlpatterns = router.urls
