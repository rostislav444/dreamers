from django.urls import reverse
from django.utils.safestring import mark_safe


def get_parent_link(obj):
    app_name = obj.__class__._meta.app_label
    model_name = obj.__class__.__name__
    parent_pk = obj.parent.pk if obj.parent else None
    verbose_name = obj.parent.name if obj.parent else None

    return mark_safe('<a href="{}">{}</a>'.format(
        reverse('admin:{}_{}_change'.format(app_name.lower(), model_name.lower()), args=(parent_pk,)), verbose_name
    ))
