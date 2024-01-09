from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from project import settings

api = [
    path('product/', include('apps.product.urls', namespace='product')),
    path('order/', include('apps.order.urls', namespace='order')),
    path('category/', include('apps.category.urls', namespace='category')),
    path('catalogue/', include('apps.catalogue.urls', namespace='catalogue')),
    path('attributes/', include('apps.attribute.urls', namespace='attributes')),
    path('newpost/', include('apps.newpost.urls', namespace='newpost')),
    path('material/', include('apps.material.urls', namespace='material')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
