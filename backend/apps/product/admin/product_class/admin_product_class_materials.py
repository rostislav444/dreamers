from django.contrib import admin

from apps.material.models import Material
from apps.product.models import ProductPartMaterialsGroups, ProductPart, ProductPartMaterials


class ProductPartMaterialsInline(admin.TabularInline):
    _obj = None

    model = ProductPartMaterials
    extra = 0

    def get_fields(self, request, obj=None):
        self._obj = obj
        fields = super().get_fields(request, obj)
        if obj:
            if obj.group.type == 'material':
                fields.remove('color')
            elif obj.group.type == 'color':
                fields.remove('material')
        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'material':
            kwargs['queryset'] = Material.objects.filter(group=self._obj.group)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProductPartMaterialsGroups)
class ProductPartMaterialsGroupsAdmin(admin.ModelAdmin):
    inlines = [
        ProductPartMaterialsInline,
    ]


class ProductPartMaterialsGroupsInline(admin.TabularInline):
    show_change_link = True
    model = ProductPartMaterialsGroups
    extra = 0


'''Product part'''


class ProductPartInline(admin.TabularInline):
    show_change_link = True
    model = ProductPart
    extra = 0


@admin.register(ProductPart)
class ProductPartAdmin(admin.ModelAdmin):
    inlines = [ProductPartMaterialsGroupsInline]
