from django.contrib import admin

from apps.product.models import Product3DBlenderModel, Lights, CameraLocations


class CameraLocationsInline(admin.TabularInline):
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
