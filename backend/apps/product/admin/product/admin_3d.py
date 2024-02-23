from django.contrib import admin

from apps.product.models import Product3DBlenderModel, Lights, CameraLocations, ProductPartScene, \
    ProductPartSceneMaterial


class ProductPartSceneMaterialInline(admin.TabularInline):
    def image_preview(self, obj):
        return '-'

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
