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

                # como na documentação da API do melhor envio está escrito que apenas os Correios e Jadlog está disponivel
                # no sandbox e a jadlog volta com duas opçoes no campo name que são .Com e .Package
                # decidi usar esse loop para por o nome da transportadora - opção disponivel 
                if item['name'] == '.Com':
                    item['name'] = 'JadeLog - Option 1'
                elif item["name"] == '.Package':
                    item["name"] = "JadeLog - Option 2"
                else: 
                    item["name"] = f'Correios - {item["name"]}'

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

class FreighInLine(admin.TabularInline):
    model = Freight
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('formated_order_number', 'amount',
                    'formated_weight', 'zip_from', 'zip_to')
    actions = [calculate_freight]
    inlines = [FreighInLine]

    def formated_order_number(self, obj):
        return obj.number
    formated_order_number.short_description = "order number"

    def formated_weight(self, obj):
        return f'{obj.weight} kg'
    formated_weight.short_description = "weight"


admin.site.register(Order, OrderAdmin)
