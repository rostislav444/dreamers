from django.contrib import admin
from django.urls import resolve
import abc


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
