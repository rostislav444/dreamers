from django.db import models

from apps.abstract.models import NameSlug
from apps.attribute.abstract.fields import OptionGroupField
from apps.attribute.abstract.models import AttributeGroupAbstract, AttributeAbstract
from apps.attribute.models import AttributeGroupUnit, AttributeGroup, Attribute
from apps.category.models import Category


class ProductClass(NameSlug):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(default='', blank=True, null=True)
    generate_sku_from_options = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def possible_option_groups(self):
        categories = self.category.get_ancestors(include_self=True)
        attributes_groups = self.product_set.all().values_list('attributes__group', flat=True)
        return AttributeGroup.objects.filter(category__in=categories).exclude(id__in=attributes_groups)

    @property
    def possible_attribute_groups(self):
        categories = self.category.get_ancestors(include_self=True)
        options_groups = self.option_groups.all().values_list('attribute_group', flat=True)
        return AttributeGroup.objects.filter(category__in=categories).exclude(id__in=options_groups)

    def save(self, *args, **kwargs):
        super(ProductClass, self).save(*args, **kwargs)


class ProductClassAttributes(AttributeAbstract):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, related_name='attributes')
    attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE,
                                        related_name='product_class')


class ProductClassProductAttributes(models.Model):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, related_name='product_attributes')
    attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE,
                                        related_name='product_class_product_attributes')


# Attribute option
class ProductClassOptionGroup(AttributeGroupAbstract):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, related_name='option_groups')
    name = models.CharField(max_length=255, default='', blank=True)
    type = OptionGroupField(max_length=24)
    attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='product_class_option_group')
    unit = models.ForeignKey(AttributeGroupUnit, on_delete=models.PROTECT, blank=True, null=True)
    save_all_options = models.BooleanField(default=False)
    image_dependency = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            ['product_class', 'name', 'attribute_group']
        ]

    def __str__(self):
        name = self.get_name
        if name:
            return name
        return '-'

    @property
    def get_name(self):
        if self.attribute_group:
            if self.attribute_group:
                return self.attribute_group.name
            else:
                return None
        return self.name

    @property
    def actual_field_name(self):
        attr_fields = {
            OptionGroupField.ATTRIBUTE: 'value_attribute',
            **self.attr_fields,
        }
        return attr_fields[self.type]

    def validate(self):
        if self.type == OptionGroupField.ATTRIBUTE:
            self.unit = None
            self.name = None
        else:
            self.attribute_group = None

    def make_save_all_options(self):
        if self.save_all_options and self.attribute_group:
            for attribute in self.attribute_group.attributes.all():
                ProductClassOption.objects.get_or_create(group=self, value_attribute=attribute)
        self.save_all_options = False

    def save(self, *args, **kwargs):
        if self.save_all_options:
            self.make_save_all_options()
        super(ProductClassOptionGroup, self).save(*args, **kwargs)


class ProductClassOption(AttributeAbstract):
    attribute_group = models.ForeignKey(ProductClassOptionGroup, on_delete=models.CASCADE, related_name="options")
    value_attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        unique_together = [
            ['attribute_group', 'value_attribute'],
            *AttributeAbstract.Meta.unique_together
        ]
        ordering = (
            'value_attribute',
            *AttributeAbstract.Meta.ordering,
        )

    @property
    def get_name(self):
        if self.value_attribute:
            return self.value_attribute.get_attribute_name
        return self.get_attribute_name

    def validator(self):
        if self.attribute_group.type != 'attribute':
            self.value_attribute = None
