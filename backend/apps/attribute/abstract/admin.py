from django.contrib import admin
import abc


class AttributeFildSet(admin.TabularInline):
    class Meta:
        abstract = True

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
