from rest_framework import routers
from apps.category import views


app_name = "category"


router = routers.DefaultRouter()
router.register(r'', views.NestedCategoryView, basename="nested_categories")


urlpatterns = [] + router.urls