from django.db import models

from apps.newpost.models import NewPostDepartments
from apps.product.models import Product, ProductClassOption, Sku


class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sku = models.ForeignKey(Sku, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
