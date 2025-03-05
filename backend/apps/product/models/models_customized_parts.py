from django.db import models


__all__ = ['ProductCustomizedPart', 'ProductCustomizedPartMaterialGroup']


class ProductCustomizedPart(models.Model):
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='customized_parts')
    part = models.ForeignKey('material.ProductPart', on_delete=models.PROTECT)
    area = models.DecimalField(default=1, decimal_places=2, max_digits=10)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.part)


class ProductCustomizedPartMaterialGroup(models.Model):
    parent = models.ForeignKey(ProductCustomizedPart, on_delete=models.CASCADE, related_name='material_groups')
    material_group = models.ForeignKey('material.MaterialGroups', on_delete=models.CASCADE)
    group_price = models.IntegerField(default=0, verbose_name='Цена, группы за м2', blank=True)
    price = models.IntegerField(default=0, verbose_name='Цена', blank=True)

    def __str__(self):
        return str(self.material_group)

    def get_price(self):
        if self.group_price:
            return self.group_price * self.parent.area
        return self.material_group.price * self.parent.area

    def save(self, *args, **kwargs):
        self.price = self.get_price()
        return super(ProductCustomizedPartMaterialGroup, self).save(*args, **kwargs)