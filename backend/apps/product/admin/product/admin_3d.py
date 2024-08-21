from django.contrib import admin
from django.utils.html import mark_safe

from apps.abstract.admin import ParentLinkMixin
from apps.product.models import Product3DBlenderModel, Lights, Camera, ProductPartScene, \
    ProductPartSceneMaterial, Product, CameraInteriorLayer, CameraInteriorLayerMaterialGroup, \
    CameraInteriorLayerMaterial, CameraInteriorLayerMaterialImage
from project.settings import MEDIA_URL


# ProductParts
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
class ProductPartSceneAdmin(ParentLinkMixin, admin.ModelAdmin):
    inlines = [ProductPartSceneMaterialInline]

    def get_model_perms(self, request):
        return {}


class ProductPartSceneInline(admin.TabularInline):
    show_change_link = True
    model = ProductPartScene
    extra = 0


# Interior
# - Interior Image
class CameraInteriorLayerMaterialImageInline(admin.TabularInline):
    def image_preview(self, obj):
        path = obj.image.image.name

        if path:
            return mark_safe(f'''
                   <img src="{MEDIA_URL}{path}" width="133" height="100" style="
                       border: 1px solid #ccc; border-radius: 6px; margin-top: -4px; object-fit: cover
                   " />
              ''')

    show_change_link = True
    model = CameraInteriorLayerMaterialImage
    fields = ['image_preview']
    readonly_fields = ['image_preview']
    extra = 0


# - Interior Material
class CameraInteriorLayerMaterialInline(admin.TabularInline):
    model = CameraInteriorLayerMaterial
    show_change_link = True
    extra = 0


@admin.register(CameraInteriorLayerMaterial)
class CameraInteriorLayerMaterialAdmin(ParentLinkMixin, admin.ModelAdmin):
    inlines = [CameraInteriorLayerMaterialImageInline]

    def get_model_perms(self, request):
        return {}


# - Interior Material Group
@admin.register(CameraInteriorLayerMaterialGroup)
class CameraInteriorLayerMaterialGroupAdmin(ParentLinkMixin, admin.ModelAdmin):
    inlines = [CameraInteriorLayerMaterialInline]

    def get_model_perms(self, request):
        return {}


class CameraInteriorLayerMaterialGroupInline(admin.TabularInline):
    model = CameraInteriorLayerMaterialGroup
    show_change_link = True
    extra = 0

# - Interior Layer
@admin.register(CameraInteriorLayer)
class CameraInteriorLayerAdmin(ParentLinkMixin, admin.ModelAdmin):
    inlines = [CameraInteriorLayerMaterialGroupInline]

    def get_model_perms(self, request):
        return {}


class CameraInteriorLayerInline(admin.TabularInline):
    model = CameraInteriorLayer
    show_change_link = True
    extra = 0


# Camera
@admin.register(Camera)
class CameraAdmin(ParentLinkMixin, admin.ModelAdmin):
    inlines = [CameraInteriorLayerInline, ProductPartSceneInline]

    def get_model_perms(self, request):
        return {}


class CameraInline(admin.TabularInline):
    show_change_link = True
    model = Camera
    extra = 0


class LightsInline(admin.TabularInline):
    model = Lights
    extra = 0


@admin.register(Product3DBlenderModel)
class Product3DBlenderModelAdmin(ParentLinkMixin, admin.ModelAdmin):
    parent_model = Product
    inlines = [CameraInline, LightsInline]

    def get_model_perms(self, request):
        return {}


class Product3DBlenderModelInline(admin.StackedInline):
    model = Product3DBlenderModel
    show_change_link = True
    extra = 0
    min_num = 1
