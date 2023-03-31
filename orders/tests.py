from django.forms import ValidationError
from django.test import TestCase
from .models import Order
# Create your tests here.
class OrderTestCase(TestCase):

    def setUp(self):
        Order.objects.create(
            number=1,
            amount=10,
            weight=2.5,
            width=30,
            height=20,
            length=40,
            zip_from='01001000',
            zip_to='04005000'
        )

    def test_order_str_method(self):
        order = Order.objects.get(number=1)
        self.assertEqual(str(order), "1")

    def test_order_zip_from_validator(self):
        invalid_order = Order(
            number=2,
            amount=5,
            weight=1.2,
            width=10,
            height=10,
            length=10,
            zip_from='invalid_zip'
        )
        with self.assertRaises(ValidationError):
            invalid_order.full_clean()

    def test_order_zip_to_validator(self):
        invalid_order = Order(
            number=3,
            amount=5,
            weight=1.2,
            width=10,
            height=10,
            length=10,
            zip_from='01001000',
            zip_to='invalid_zip'
        )
        with self.assertRaises(ValidationError):
            invalid_order.full_clean()

    def test_order_fields(self):
        order = Order.objects.get(number=1)
        self.assertEqual(order.amount, 10)
        self.assertEqual(order.weight, 2.5)
        self.assertEqual(order.width, 30)
        self.assertEqual(order.height, 20)
        self.assertEqual(order.length, 40)
        self.assertEqual(order.zip_from, '01001000')
        self.assertEqual(order.zip_to, '04005000')