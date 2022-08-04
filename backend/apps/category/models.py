from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from apps.abstract.models import NameSlug
from django.utils.translation import gettext_lazy as _


class Category(MPTTModel, NameSlug):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name']


class Properties(NameSlug):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)
