from django.db import models
from warehouses.models import Warehouse

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    size = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='products')
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    
    
class Delivery(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    
    amount = models.IntegerField(null=True, blank=True)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    status = models.BooleanField()
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    