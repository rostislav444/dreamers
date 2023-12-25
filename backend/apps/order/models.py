from random import choices

from django.db import models
from apps.product.models import Product, ProductClassOption, Sku
from apps.newpost.models import NewPostDepartments


class Order(models.Model):
    DELIVERY_TYPES = (
        ('0', 'Адресная доставка'),
        ('1', 'Новая почта')
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_type = models.CharField(choices=DELIVERY_TYPES, default='0', max_length=1)

    def __str__(self):
        return str(self.created_at)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, related_name='order_product_sku')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)

    @property
    def get_price(self):
        price = 0
        if self.options.count():
            price = self.product.price
            for option in self.options.all():
                attribute_group = option.option.attribute_group.attribute_group
                attribute = option.option.value_attribute
                price_required = attribute_group.price_required
                if price_required == 'attribute':
                    price += attribute.price
        return price

    @property
    def get_total(self):
        return self.price * self.quantity

    @property
    def get_image(self):
        image = self.sku.images.first()
        if image:
            return image.image
        return None

    def save(self, *args, **kwargs):
        self.price = self.get_price
        super(OrderProduct, self).save(*args, **kwargs)


class OrderProductOptions(models.Model):
    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE, related_name='options')
    option = models.ForeignKey(ProductClassOption, on_delete=models.SET_NULL, null=True, blank=True)
    option_value = models.JSONField(default=dict)


class OrderNewPostDelivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='newpost')
    department = models.ForeignKey(NewPostDepartments, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Доставка Новой Почтой'
        verbose_name_plural = 'Доставка Новой Почтой'


class OrderAddressDelivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='address')
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    apartment = models.PositiveIntegerField(null=True, blank=True)
    floor = models.PositiveIntegerField(null=True, blank=True)
    entrance = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Адресная доставка'
        verbose_name_plural = 'Адресная доставка'
