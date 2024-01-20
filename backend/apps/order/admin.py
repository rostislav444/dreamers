from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe

from apps.order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    def image_tag(self, instance):
        sku_image = instance.sku.images.first()

        if sku_image:
            sku_admin_url = reverse('admin:product_sku_change', args=[sku_image.sku.id])
            image_html = f'''
                   <a href="{sku_admin_url}" target="_blank">
                       <img src="{sku_image.image.url}" width="120" height="80" style="
                           border: 1px solid #ccc; border-radius: 6px; margin-top: -4px; object-fit: cover
                       " />
                   </a>
               '''
            return mark_safe(image_html)
        return '-'

    def sku_data(self, instance):
        values = []
        for material in instance.sku.materials.all():
            value = f'<li>{material.get_material_part_name}: {str(material.material)}</li>'
            values.append(value)

        return mark_safe(f'<ul>{"".join(values)}</ul>')

    def item_sum(self, instance):
        return instance.quantity * instance.price

    image_tag.short_description = 'Изображение'
    sku_data.short_description = 'Характеристики'
    item_sum.short_description = 'Сумма'

    fields = ('image_tag', 'sku_data', 'quantity', 'price', 'item_sum')
    readonly_fields = ('image_tag', 'sku_data', 'item_sum', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
