from abc import ABC, abstractmethod

from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from django.utils.safestring import mark_safe
from django.db import models

# Register your models here.
class GetParentFromRequestAbstract:
    class Meta:
        abstract = True

    def get_max_num(self, request, obj=None, **kwargs):
        if not obj:
            return 0

    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            return self.parent_model.objects.get(pk=resolved.kwargs['object_id'])
        return None


# Place at the start og your class inline arguments
class ParentLinkMixin:
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ParentLinkMixin, self).__init__(*args, **kwargs)

        for field in self.model._meta.get_fields():
            if isinstance(field, models.ForeignKey) and field.remote_field.model == self.parent_model:
                self.parent_model_field_name = field.name

    @property
    @abstractmethod
    def parent_model(self):
        pass

    def parent_link(self, obj=None, **kwargs):
        app_name = self.parent_model._meta.app_label
        model_name = self.parent_model.__name__
        verbose_name = model_name

        if hasattr(self.parent_model._meta, 'verbose_name'):
            verbose_name = self.parent_model._meta.verbose_name

        return mark_safe('<a href="{}">{}</a>'.format(
            reverse('admin:{}_{}_change'.format(app_name.lower(), model_name.lower()),
                    args=(getattr(obj, self.parent_model_field_name).pk,)
                    ),
            verbose_name
        ))

    def response_change(self, request, obj, post_url_continue=None):
        app_name = self.parent_model._meta.app_label
        model_name = self.parent_model.__name__

        if "_continue" in request.POST:
            return super(ParentLinkMixin, self).response_change(request, obj)

        return HttpResponseRedirect(
            reverse('admin:{}_{}_change'.format(app_name.lower(), model_name.lower()),
                args=(getattr(obj, self.parent_model_field_name).pk,)
            )
        )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ParentLinkMixin, self).get_fieldsets(request, obj)

        if fieldsets and len(fieldsets) > 0 and len(fieldsets[0]) > 0:
            if 'parent_link' in fieldsets[0][1]['fields']:
                fieldsets[0][1]['fields'].remove('parent_link')
            fieldsets[0][1]['fields'] = ['parent_link', *fieldsets[0][1]['fields']]
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(ParentLinkMixin, self).get_readonly_fields(request, obj)
        if readonly_fields:
            return ['parent_link', *readonly_fields]
        else:
            return ['parent_link']
