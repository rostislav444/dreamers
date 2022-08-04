import abc

from django.contrib import admin
from django.db.models import Q
from apps.category.models import Category, Properties
from apps.attribute.models import AttributeGroup, PredefinedOptionsGroups, PredefinedAttributeGroups
from apps.abstract.admin import GetParentFromRequestAbstract


class AttributeGroupInline(admin.TabularInline):
    show_change_link = True
    model = AttributeGroup
    extra = 0


class PropertiesInline(admin.TabularInline):
    model = Properties
    extra = 0


class PredefinedAttributeGroupsAbstract(GetParentFromRequestAbstract, admin.TabularInline):
    extra = 0

    class Meta:
        abstract = True

    @property
    @abc.abstractmethod
    def opponent_model(self):
        pass

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(PredefinedAttributeGroupsAbstract, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'group':
            if request:
                category = self.get_parent_object_from_request(request)
                ancestors_ids = category.get_ancestors(include_self=True).values_list('id', flat=True)
                field.queryset = field.queryset.filter(Q(category__id__in=ancestors_ids) | Q(category=None)).exclude(
                    id__in=self.opponent_model.objects.filter(category__in=ancestors_ids, name=None).values_list(
                        'group', flat=True)
                )
        return field


class PredefinedAttributeGroupsInline(PredefinedAttributeGroupsAbstract):
    model = PredefinedAttributeGroups
    opponent_model = PredefinedOptionsGroups


class PredefinedOptionsGroupsInline(PredefinedAttributeGroupsAbstract):
    model = PredefinedOptionsGroups
    opponent_model = PredefinedAttributeGroups



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        AttributeGroupInline,
        PredefinedAttributeGroupsInline,
        PredefinedOptionsGroupsInline
    ]
