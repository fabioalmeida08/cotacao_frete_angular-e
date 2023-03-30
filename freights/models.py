from django.db import models
from orders.models import Order
# Create your models here.


class Freight(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    carrier = models.CharField(max_length=255)
    delivery_time = models.PositiveIntegerField()
    delivery_cost = models.FloatField()
    external_freight_id = models.PositiveIntegerField()
