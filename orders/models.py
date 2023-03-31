from django.db import models
import uuid
from django.core import validators


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.PositiveBigIntegerField(verbose_name="Order number")
    amount = models.PositiveIntegerField()
    weight = models.FloatField(verbose_name="Weight (kg)")
    width = models.PositiveIntegerField(verbose_name='Width (cm)')
    height = models.PositiveIntegerField(verbose_name='Height (cm)')
    length = models.PositiveIntegerField(verbose_name='Lenght in (cm)')
    zip_from = models.CharField(max_length=10, validators=[validators.RegexValidator(r'[0-9]+$', 'Enter a valid zip code.')])
    zip_to = models.CharField(max_length=10, validators=[validators.RegexValidator(r'[0-9]+$', 'Enter a valid zip code.')])

    def __str__(self):
        return f'{self.number}'
