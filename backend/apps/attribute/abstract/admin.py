from django.contrib import admin
from django.utils.html import mark_safe

from apps.attribute.abstract.fields import AttributeGroupTypeAbstractField
from apps.attribute.models import AttributeGroup, AttributeSubGroup
from apps.product.models import ProductClassOptionGroup


class AttributeFildSet(admin.TabularInline):
    class Meta:
        abstract = True

    def image_tag(self, instance):
        path = None
        if instance.value_image_image.path:
            path = instance.value_image_image.name
        elif instance.value_image_image.path:
            path = instance.value_image_image.name
        if path:
            return mark_safe(f'''
                 <img src="/media/{path}" width="80" height="80" style="
                     border: 1px solid #ccc; border-radius: 6px; margin-top: -4px; object-fit: cover
                 " />
            ''')
        return None

    image_tag.short_description = 'Image'

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return super(AttributeFildSet, self).get_readonly_fields(request, obj)
        readonly_fields = list(super(AttributeFildSet, self).get_readonly_fields(request, obj))

        if isinstance(obj, AttributeSubGroup):
            obj = obj.group

        if obj.type in ['color', 'image']:
            if 'image_tag' not in readonly_fields:
                readonly_fields.append('image_tag')
        return tuple(readonly_fields)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(AttributeFildSet, self).get_fieldsets(request, obj)
        fields = []
        for field in fieldsets[0][1]['fields']:
            if not field.startswith('value_') and field not in ['color']:
                fields.append(field)
        if obj:
            print(obj.__class__.__name__)
            if isinstance(obj, AttributeSubGroup):
                obj = obj.group
                fields.remove('attribute_group')

            if isinstance(obj, ProductClassOptionGroup):
                obj = obj.attribute_group

            fields.append(obj.actual_field_name)
            if hasattr(obj, 'has_color') and obj.has_color:
                fields.append('color')
            if obj.type == AttributeGroupTypeAbstractField.IMAGE:
                if 'manual' in fields:
                    fields.remove('manual')
            if obj.price_required == AttributeGroup.PRICE_RQ_SUB_GROUP:
                fields.remove('price')

        fieldsets[0][1]['fields'] = fields
        return fieldsets
