from django.contrib import admin

from apps.product.models import ProductCustomizedPart, ProductCustomizedPartMaterialGroup

__all__ = ['ProductCustomizedPartMaterialGroupAdmin', 'ProductCustomizedPartAdmin', 'ProductCustomizedPartInline']


@admin.register(ProductCustomizedPartMaterialGroup)
class ProductCustomizedPartMaterialGroupAdmin(admin.ModelAdmin):
    pass


class ProductCustomizedPartMaterialGroupInline(admin.TabularInline):
    model = ProductCustomizedPartMaterialGroup
    extra = 0


@admin.register(ProductCustomizedPart)
class ProductCustomizedPartAdmin(admin.ModelAdmin):
    inlines = [ProductCustomizedPartMaterialGroupInline]


class ProductCustomizedPartInline(admin.TabularInline):
    model = ProductCustomizedPart
    readonly_fields = ['part']
    show_change_link = True
    extra = 0

    def __init__(self, *args, **kwrgs):
        self.materials_set = None
        super().__init__(*args, **kwrgs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'part' and self.materials_set:
            kwargs['queryset'] = self.materials_set.parts.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def calc_num(self, obj):
        if not obj:
            return 0
        self.materials_set = obj.product_class.materials_set
        if self.materials_set:
            return self.materials_set.parts.count()
        return 0

    def get_min_num(self, request, obj=None, **kwargs):
        return self.calc_num(obj)

    def get_max_num(self, request, obj=None, **kwargs):
        return self.calc_num(obj)
