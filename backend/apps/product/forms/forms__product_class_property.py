from django.db.models import Q
from django.forms import BaseInlineFormSet, ModelForm
from apps.category.models import Properties
from apps.product.models import ProductClassProperty


class ProductClassPropertyInlineAdminFrom(ModelForm):
    class Meta:
        model = ProductClassProperty
        fields = ['property', 'name']

    def __init__(self, *args, **kwargs):
        super(ProductClassPropertyInlineAdminFrom, self).__init__(*args, **kwargs)
        keys = kwargs.keys()
        if 'initial' in keys:
            property_id = kwargs['initial']['property']
        elif 'instance' in keys:
            property_id = kwargs['instance'].property.id
        else:
            property_id = None
        if property_id:
            self.fields['property'].queryset = self.fields['property'].queryset.filter(id=property_id)
        else:
            self.fields['property'].queryset = self.fields['property'].queryset.none()
        self.fields['property'].empty_label = None


class ProductClassPropertyAdminFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        product_class = kwargs['instance']
        if product_class.pk:
            categories = product_class.category.get_ancestors(include_self=True)
            properties = Properties.objects.filter(Q(category=None) | Q(category__in=categories))
            count = properties.count()
            self.min_num = count
            self.max_num = count
            exist_ids = product_class.properties.all().values_list('property__id', flat=True)
            kwargs.update({'initial': [{'property': item.pk} for item in properties.exclude(id__in=exist_ids)]})
        super(ProductClassPropertyAdminFormSet, self).__init__(*args, **kwargs)