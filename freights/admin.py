from django.contrib import admin
from .models import Freight


class FreightAdmin(admin.ModelAdmin):
    list_display = ('formated_order', 'carrier',
                    'formated_delivery_time', 'formated_delivery_cost')

    def formated_order(self, obj):
        return obj.order
    formated_order.short_description = 'order number'

    def formated_delivery_cost(self, obj):
        return f'R$ {obj.delivery_cost}'
    formated_delivery_cost.short_description = 'Delivery Cost'

    def formated_delivery_time(self, obj):
        return f'{obj.delivery_time} days'
    formated_delivery_time.short_description = "Delivery time"

admin.site.register(Freight, FreightAdmin)
