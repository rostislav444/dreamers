from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('apps.product.urls', namespace='product')),
    path('category/', include('apps.category.urls', namespace='category')),
    path('catalogue/', include('apps.catalogue.urls', namespace='catalogue')),
    path('attribute/', include('apps.attribute.urls', namespace='attribute')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
