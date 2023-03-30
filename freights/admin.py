from django.contrib import admin
from .models import Freight


class FreightAdmin(admin.ModelAdmin):
    list_display = ('formated_order', 'carrier', 'delivery_time', 'delivery_cost')

    def formated_order(self, obj):
        return obj.order
    formated_order.short_description = 'order number'

admin.site.register(Freight, FreightAdmin)
