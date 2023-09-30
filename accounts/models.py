from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    status = models.BooleanField(default=False)
    role = models.CharField(max_length=100, default='s_admin')

    def __str__(self) -> str:
        return f"{self.username}"

    def save(self, **kwargs):
        super().save(**kwargs)
        self.password = make_password(self.password)


class DeviceToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
