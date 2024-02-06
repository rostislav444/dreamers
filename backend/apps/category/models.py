from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from apps.abstract.models import NameSlug


class Category(MPTTModel, NameSlug):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        names = [c.name for c in self.get_ancestors(include_self=True)]

        return ' > '.join(names)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name']


class Properties(NameSlug):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)


class CategoryAttributeGroup(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attribute_groups')
    attribute_group = models.ForeignKey('attribute.AttributeGroup', on_delete=models.CASCADE,
                                        related_name='category_attribute_groups')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('Category Attribute Group')
        verbose_name_plural = _('Category Attribute Groups')
        unique_together = ('category', 'attribute_group')

    def __str__(self):
        if hasattr(self, 'category'):
            return f'{self.category} - {self.attribute_group}'
        return '-'


class Collection(NameSlug):
    def __str__(self):
        return self.name

