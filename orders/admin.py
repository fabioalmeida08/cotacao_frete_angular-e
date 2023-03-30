from django.contrib import admin
from .models import Order
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'amount',
                    'weight', 'zip_from', 'zip_to')


admin.site.register(Order, OrderAdmin)
