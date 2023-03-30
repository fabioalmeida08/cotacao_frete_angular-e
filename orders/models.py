from django.db import models
import uuid
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.PositiveBigIntegerField()
    amount = models.PositiveIntegerField()
    weight = models.FloatField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    length = models.PositiveIntegerField()
    zip_from = models.CharField(max_length=10)
    zip_to = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.number}'