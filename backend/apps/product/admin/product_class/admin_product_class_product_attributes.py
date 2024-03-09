from django.contrib import admin

from apps.attribute.models import Attribute
from apps.product.abstract.admin import FilterAttributeGroupsFK
from apps.product.forms import ProductClassProductAttributeGroupsForm
from apps.product.models import ProductClassProductAttributeGroups, ProductClassProductAttributes


# Product class page
class ProductClassProductAttributeGroupsInline(admin.TabularInline, FilterAttributeGroupsFK):
    model = ProductClassProductAttributeGroups
    form = ProductClassProductAttributeGroupsForm
    show_change_link = True
    extra = 0


# Product class product attributes admin
class ProductClassProductAttributesInline(admin.TabularInline):
    model = ProductClassProductAttributes
    extra = 0

    def __init__(self, *args, **kwargs):
        self.group = None
        super(ProductClassProductAttributesInline, self).__init__(*args, **kwargs)

    def get_max_num(self, request, obj=None, **kwargs):
        self.group = obj.attribute_group
        if obj.use_all_attributes:
            return 0
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "attribute" and self.group:
            kwargs["queryset"] = Attribute.objects.filter(attribute_group=self.group)
        else:
            kwargs["queryset"] = Attribute.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProductClassProductAttributeGroups)
class ProductClassProductAttributeGroupsAdmin(admin.ModelAdmin):
    inlines = [ProductClassProductAttributesInline]

    def get_model_perms(self, request):
        return {}
