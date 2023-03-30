from django.contrib import admin
from .models import Order
import requests
import json
import os
from dotenv import load_dotenv
from freights.models import Freight
from django.contrib import messages

load_dotenv()


def calculate_freight(modeladmin, request, queryset):
    
    # informaçoes para o request
    token = os.environ.get("TOKEN")
    url = "https://sandbox.melhorenvio.com.br/api/v2/me/shipment/calculate"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    # loopar por todos o items do queryset e serializar em json
    for order in queryset:
        payload = {
            "from": {
                "postal_code": order.zip_from
            },
            "to": {
                "postal_code": order.zip_to
            },
            "package":
                {
                    "weight": order.weight,
                    "width": order.width,
                    "height": order.height,
                    "length": order.length
            },
            "options": {
                "insurance_value": 100.00,
                "own_hand": False,
                "receipt": True
            },
            "services": "1,2,3,4"
        }

        payload = json.dumps(payload)

        # fazer o request
        response = requests.request("POST", url, headers=headers, data=payload)
        
        # deserializar o json 
        response_dict = json.loads(response.text)

        # caso a resposta http seja 200 criar um entrada para freight
        if response.status_code == 200:
            for item in response_dict:

                freight = Freight(
                    order=order,
                    carrier=item["name"],
                    delivery_time=item["delivery_time"],
                    delivery_cost=item["price"],
                    external_freight_id=item["id"]
                )

                freight.save()

            messages.success(
                request, f'Fretes calculados para o pedido {order.number}')

        else:
            messages.error(
                request, f'Erro ao calcular fretes para o pedido {order.number}')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('formated_order_number', 'amount',
                    'weight', 'zip_from', 'zip_to')
    actions = [calculate_freight]

    def formated_order_number(self, obj):
        return obj.number
    formated_order_number.short_description = "order number"


admin.site.register(Order, OrderAdmin)
