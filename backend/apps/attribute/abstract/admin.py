from django.contrib import admin


class AttributeFildSet(admin.TabularInline):
    class Meta:
        abstract = True

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(AttributeFildSet, self).get_readonly_fields(request, obj))
        if obj.type in ['color', 'image']:
            if 'image_tag' not in readonly_fields:
                readonly_fields.append('image_tag')
        return tuple(readonly_fields)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(AttributeFildSet, self).get_fieldsets(request, obj)
        fields = []
        for field in fieldsets[0][1]['fields']:
            if not field.startswith('value_'):
                fields.append(field)
        if obj:
            fields.append(obj.actual_field_name)

        fieldsets[0][1]['fields'] = fields
        return fieldsets
