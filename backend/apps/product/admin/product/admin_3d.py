from django.contrib import admin
from django.utils.html import mark_safe

from apps.product.models import Product3DBlenderModel, Lights, CameraLocations, ProductPartScene, \
    ProductPartSceneMaterial
from project.settings import MEDIA_URL


class ProductPartSceneMaterialInline(admin.TabularInline):
    def image_preview(self, obj):
        path = obj.image.image.name

        if path:
            return mark_safe(f'''
                   <img src="{MEDIA_URL}{path}" width="133" height="100" style="
                       border: 1px solid #ccc; border-radius: 6px; margin-top: -4px; object-fit: cover
                   " />
              ''')

    show_change_link = True
    model = ProductPartSceneMaterial
    fields = ['material', 'image_preview']
    readonly_fields = ['material', 'image_preview']
    extra = 0


@admin.register(ProductPartScene)
class ProductPartSceneAdmin(admin.ModelAdmin):
    inlines = [ProductPartSceneMaterialInline]


class ProductPartSceneInline(admin.TabularInline):
    show_change_link = True
    model = ProductPartScene
    extra = 0


@admin.register(CameraLocations)
class CameraLocationsAdmin(admin.ModelAdmin):
    inlines = [ProductPartSceneInline]


class CameraLocationsInline(admin.TabularInline):
    show_change_link = True
    model = CameraLocations
    extra = 0


class LightsInline(admin.TabularInline):
    model = Lights
    extra = 0


@admin.register(Product3DBlenderModel)
class Product3DBlenderModelAdmin(admin.ModelAdmin):
    inlines = [CameraLocationsInline, LightsInline]


class Product3DBlenderModelInline(admin.StackedInline):
    model = Product3DBlenderModel
    show_change_link = True
    extra = 0
    min_num = 1
