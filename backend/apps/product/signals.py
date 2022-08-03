from django.db.models import signals
from django.dispatch import receiver
from apps.attribute.abstract.fields import AttributeGroupTypeAbstractField
from apps.attribute.models import AttributeGroup
from apps.product.models import ProductClass, ProductClassOptionGroup


@receiver(signals.post_save, sender=ProductClass)
def add_required_options_to_product_class(sender, instance, **kwargs):
    for attribute_group in instance.category.attribute_groups.filter(required=AttributeGroup.OPTION):
        params = {
            'product_class': instance,
            'type': AttributeGroupTypeAbstractField.ATTRIBUTE,
            'attribute_group': attribute_group
        }
        try:
            ProductClassOptionGroup.objects.get(**params)
        except ProductClassOptionGroup.DoesNotExist:
            product_class = ProductClassOptionGroup(**params)
            product_class.save()


# @receiver(signals.post_save, sender=ProductClassOptionGroup)
# def run_save_all_options(sender, instance, **kwargs):
#     if instance.save_all_options and instance.attribute_group:
#         for attr in instance.attribute_group.attributes.all():
#             params = {
#                 'group': instance,
#                 'value_attribute': attr
#             }
#             try:
#                 ProductClassOption.objects.get(**params)
#             except ProductClassOption.DoesNotExist:
#                 option = ProductClassOption(**params)
#                 option.save()
