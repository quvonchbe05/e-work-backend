from django.db import models
from django.db.models import CASCADE

from accounts.models import CustomUser


# Create your models here.
class Car(models.Model):
    car_name = models.CharField(max_length=100)
    car_number = models.CharField(max_length=100)
    driver = models.ForeignKey(CustomUser, on_delete=CASCADE)
    car_size = models.FloatField()