from django.db import models
from objects.models import Object
from products.models import TemplateProduct
from warehouses.models import Warehouse

# Create your models here.
class Bid(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='bids')
    status = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.object.name)
    
class BidProduct(models.Model):
    product = models.ForeignKey(TemplateProduct, on_delete=models.CASCADE)
    amount = models.IntegerField()
    
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='products')
    
    def __str__(self) -> str:
        return str(self.product.name)
    
    
    
    
    
class BidToWarehouse(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='bidsToWarehouse')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='bidsToWarehouse')
    status = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.object.name)
    
class BidProductToWarehouse(models.Model):
    product = models.ForeignKey(TemplateProduct, on_delete=models.CASCADE)
    amount = models.IntegerField()
    
    bid = models.ForeignKey(BidToWarehouse, on_delete=models.CASCADE, related_name='products')
    
    def __str__(self) -> str:
        return str(self.product.name)
    