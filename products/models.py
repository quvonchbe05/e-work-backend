from django.db import models
from warehouses.models import Warehouse

# Create your models here.
class Delivery(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    
    status = models.BooleanField()
    
    def __str__(self) -> str:
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    size = models.CharField(max_length=50)
    price = models.CharField(max_length=155, null=True, blank=True)
    total_price = models.CharField(max_length=255, null=True, blank=True)
    
    date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    
    description = models.TextField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    
    
    