from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'amount',
                    'weight', 'zip_from', 'zip_to')


admin.site.register(Order, OrderAdmin)
