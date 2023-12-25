from django.contrib import admin
from django.template import loader
from django.utils.html import mark_safe

from apps.order.models import Order, OrderProduct, OrderNewPostDelivery, OrderAddressDelivery
from apps.order.serializers import AdminOrderProductOptionsSerializer


class OrderAddressDeliveryInline(admin.StackedInline):
    model = OrderAddressDelivery
    extra = 0


class OrderNewPostDeliveryInline(admin.StackedInline):
    model = OrderNewPostDelivery
    extra = 0


class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    extra = 0

    @staticmethod
    def current_price(obj=None):
        if obj:
            return obj.get_price
        return None

    @staticmethod
    def total(obj=None):
        if obj:
            return obj.get_total
        return None

    @staticmethod
    def image(obj=None):
        if obj:
            return mark_safe(f'''
                 <img src="/media/{obj.get_image}" width="160" height="160" style="
                     border: 1px solid #ccc; border-radius: 6px; margin-top: -4px; object-fit: cover
                 " />
            ''')
        return None

    @staticmethod
    def options_data(obj=None):
        if obj:
            template = loader.get_template('admin/order/options_data.html')
            context = {
                'options': AdminOrderProductOptionsSerializer(obj.options.all(), many=True).data,
            }
            return mark_safe(template.render(context))

    fieldsets = (
        (None, {
            'fields': ('image', 'product', 'quantity', ('price', 'current_price'), 'total', 'discount', 'options_data')
        }),
    )

    readonly_fields = ('current_price', 'total', 'image', 'options_data')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderProductInline
    ]

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj=None)
        if obj.delivery_type == '0':
            inlines.insert(0, OrderAddressDeliveryInline(self.model, self.admin_site))
        if obj.delivery_type == '1':
            inlines.insert(0, OrderNewPostDeliveryInline(self.model, self.admin_site))
        return inlines