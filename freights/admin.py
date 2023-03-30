from django.contrib import admin
from .models import Freight


class FreightAdmin(admin.ModelAdmin):
    list_display = ('order', 'carrier', 'delivery_time', 'delivery_cost')


admin.site.register(Freight, FreightAdmin)
