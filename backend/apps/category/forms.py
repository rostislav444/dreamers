from django import forms
from apps.category.models import CategoryAttributeGroup


class CategoryAttributeGroupForm(forms.ModelForm):
    class Meta:
        model = CategoryAttributeGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryAttributeGroupForm, self).__init__(*args, **kwargs)


class CategoryAttributeGroupFormSet(forms.BaseInlineFormSet):
    class Meta:
        model = CategoryAttributeGroup

    # def __init__(self, *args, **kwargs):
    #     super(CategoryAttributeGroupFormSet, self).__init__(*args, **kwargs)
    #     instance = kwargs.get('instance')
    #
    #     if instance:
    #         ancestors = instance.get_ancestors(include_self=False)
    #         self.queryset = self.queryset.exclude(category__in=ancestors)
    #     else:
    #         self.queryset = self.queryset.none()






