from django.db import models

# Create your models here.
class Driver(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=155)
    phone = models.CharField(max_length=15)
    status = models.BooleanField(default=False)
    
    
    def __str__(self) -> str:
        return f"{self.name}"