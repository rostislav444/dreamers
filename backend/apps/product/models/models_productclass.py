from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.abstract.fields import CustomFileField
from apps.abstract.models import NameSlug
from apps.attribute.abstract.fields import OptionGroupField
from apps.attribute.abstract.models import AttributeGroupAbstract, AttributeAbstractWithValueAttribute
from apps.attribute.models import AttributeGroupUnit, AttributeGroup, Attribute, AttributeSubGroup
from apps.category.models import Category, Collection
from apps.material.models.models_material_set import MaterialsSet
from apps.product.utils import generate_variants_from_dimensions


class ProductClass(NameSlug):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    collection = models.ForeignKey(Collection, null=True, blank=True, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(default='', blank=True, null=True)
    materials_set = models.ForeignKey(MaterialsSet, on_delete=models.PROTECT, null=True, blank=True)
    images_by_sku = models.BooleanField(default=False)

    # Width
    min_width = models.PositiveIntegerField(_('Width'), default=0)
    max_width = models.PositiveIntegerField(_('Max width'), blank=True, null=True)
    width_step = models.PositiveIntegerField(_('Width step'), blank=True, null=True)
    # Height
    min_height = models.PositiveIntegerField(_('Height'), default=0)
    max_height = models.PositiveIntegerField(_('Max height'), blank=True, null=True)
    height_step = models.PositiveIntegerField(_('Height step'), blank=True, null=True)
    # Depth
    min_depth = models.PositiveIntegerField(_('Depth'), default=0)
    max_depth = models.PositiveIntegerField(_('Max depth'), blank=True, null=True)
    depth_step = models.PositiveIntegerField(_('Depth step'), blank=True, null=True)

    # Initial price
    initial_price = models.PositiveIntegerField(_('Initial price'), default=0)
    square_decimeter_price = models.PositiveIntegerField(_('Square decimeter price'), default=0)

    # Booleans
    generate_sku_from_options = models.BooleanField(default=False, verbose_name='Сгенерировать Sku и сочетания цветов')
    generate_variants_from_sizes = models.BooleanField(default=False, verbose_name='Сгенерировать варианты из размеров')

    def __str__(self):
        return self.name

    @property
    def possible_option_groups(self):
        categories = self.category.get_ancestors(include_self=True)
        attributes_groups = self.products.all().values_list('attributes__group', flat=True)
        return AttributeGroup.objects.filter(category__in=categories).exclude(id__in=attributes_groups)

    @property
    def possible_attribute_groups(self):
        categories = self.category.get_ancestors(include_self=True)
        return AttributeGroup.objects.filter(category_attribute_groups__category__in=categories)

    def _get_attribute_groups(self, filter_conditions):
        categories = self.category.get_ancestors(include_self=True)
        exists = AttributeGroup.objects.filter(filter_conditions).distinct()
        return AttributeGroup.objects.filter(category_attribute_groups__category__in=categories).exclude(
            Q(id__in=exists.values_list('id', flat=True)) | Q(slug__in=exists.values_list('slug', flat=True)))

    @property
    def attr_groups_for_product_class_attributes(self):
        return self._get_attribute_groups(
            Q(product_class_option_group__product_class=self) | Q(product_class_product_attributes__product_class=self))

    @property
    def attr_groups_for_product_class_options(self):
        return self._get_attribute_groups(
            Q(product_class_attributes__product_class=self) | Q(product_class_product_attributes__product_class=self))

    @property
    def attr_groups_for_product_class_product_attributes(self):
        return self._get_attribute_groups(
            Q(product_class_attributes__product_class=self) | Q(product_class_option_group__product_class=self))

    def save(self, *args, **kwargs):
        super(ProductClass, self).save(*args, **kwargs)

        if self.generate_variants_from_sizes:
            generate_variants_from_dimensions(self)


class ProductClass3DBlenderModel(models.Model):
    product_class = models.OneToOneField(ProductClass, on_delete=models.CASCADE, related_name='model_3d')
    blend = CustomFileField(validators=[FileExtensionValidator(allowed_extensions=["blend"])])


'''Attributes'''


class ProductClassAttributes(models.Model):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, related_name='attributes')
    attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE,
                                        related_name='product_class_attributes')
    value_attribute = models.ForeignKey('attribute.Attribute', on_delete=models.PROTECT, blank=True, null=True)


class ProductClassProductAttributeGroups(models.Model):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, related_name='product_attributes_groups')
    attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE,
                                        related_name='product_class_product_attributes')
    use_all_attributes = models.BooleanField(default=True)

    def __str__(self):
        if self.attribute_group:
            return self.attribute_group.name
        return '-'


class ProductClassProductAttributes(models.Model):
    attribute_group = models.ForeignKey(ProductClassProductAttributeGroups, on_delete=models.CASCADE,
                                        related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name='product_class_attributes')

    class Meta:
        unique_together = [
            ['attribute_group', 'attribute']
        ]

    def __str__(self):
        unit = self.attribute_group.attribute_group.unit
        if unit:
            return str(self.attribute) + ' ' + unit.name
        return str(self.attribute)


'''Options'''


class ProductClassOptionGroup(AttributeGroupAbstract):
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, related_name='option_groups')
    name = models.CharField(max_length=255, default='', blank=True)
    type = OptionGroupField(max_length=24)
    attribute_group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='product_class_option_group')
    attribute_sub_group = models.ManyToManyField(AttributeSubGroup, blank=True)
    unit = models.ForeignKey(AttributeGroupUnit, on_delete=models.PROTECT, blank=True, null=True)
    model_3d_name = models.CharField(blank=True, null=True, max_length=255)

    w = models.BooleanField(default=False)
    h = models.BooleanField(default=False)
    d = models.BooleanField(default=False)

    mlt = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    use_all_options = models.BooleanField(default=False)
    option_price_required = models.BooleanField(default=False)

    image_dependency = models.BooleanField(default=False)

    class Meta:
        unique_together = [
            ['product_class', 'name', 'attribute_group']
        ]
        ordering = ['name']

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

    def _option_price_required_changed_action(self):
        if self.use_all_options:
            if self.option_price_required:
                objects = []
                for attribute in self.attribute_group.attributes.all():
                    try:
                        ProductClassOption.objects.get(attribute_group=self, value_attribute=attribute)
                    except ObjectDoesNotExist:
                        objects.append(ProductClassOption(attribute_group=self, value_attribute=attribute))
                if len(objects):
                    ProductClassOption.objects.bulk_create(objects)
            else:
                self.options.all().delete()

    def _run_after_save(self):
        self._option_price_required_changed_action()

    def save(self, *args, **kwargs):
        super(ProductClassOptionGroup, self).save(*args, **kwargs)
        self._run_after_save()


class ProductClassOption(AttributeAbstractWithValueAttribute):
    attribute_group = models.ForeignKey(ProductClassOptionGroup, on_delete=models.CASCADE, related_name="options")
    value_attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, blank=True, null=True,
                                        related_name='product_class_options')
    price = models.PositiveIntegerField(default=0, blank=True, null=True)
