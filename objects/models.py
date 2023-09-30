from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Object(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    worker = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='object', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
