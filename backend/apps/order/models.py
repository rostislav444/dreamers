from django.db import models

from apps.newpost.models import NewPostDepartments
from apps.product.models import Product, ProductClassOption, Sku


class Order(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Фамилия')
    father_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Отчество')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='E-mail')
    city = models.CharField(max_length=255, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        formatted_date = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return f"Заказ #{self.id} - {formatted_date}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    sku = models.ForeignKey(Sku, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.sku.product.product_class.name

    def get_image(self):
        return '-'


class OrderItemMaterials(models.Model):
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey('material.ProductPartMaterials', on_delete=models.CASCADE)


