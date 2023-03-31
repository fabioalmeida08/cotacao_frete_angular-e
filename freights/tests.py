from django.test import TestCase
from orders.models import Order
from .models import Freight
# Create your tests here.
class FreightTestCase(TestCase):

    def setUp(self):
        order = Order.objects.create(
            number=2,
            amount=10,
            weight=2.5,
            width=30,
            height=20,
            length=40,
            zip_from='01001000',
            zip_to='04005000'
        )
        Freight.objects.create(
            order=order,
            carrier='Correios - SEDEX',
            delivery_time=3,
            delivery_cost=50.0,
            external_freight_id=123
        )

    def test_freight_fields(self):
        freight = Freight.objects.get(id=1)
        self.assertEqual(freight.order.amount, 10)
        self.assertEqual(freight.order.weight, 2.5)
        self.assertEqual(freight.order.width, 30)
        self.assertEqual(freight.order.height, 20)
        self.assertEqual(freight.order.length, 40)
        self.assertEqual(freight.order.zip_from, '01001000')
        self.assertEqual(freight.order.zip_to, '04005000')
        self.assertEqual(freight.carrier, 'Correios - SEDEX')
        self.assertEqual(freight.delivery_time, 3)
        self.assertEqual(freight.delivery_cost, 50.0)
        self.assertEqual(freight.external_freight_id, 123)