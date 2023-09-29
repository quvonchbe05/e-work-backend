from django.db import models

from objects.models import Object
from products.models import TemplateProduct
from warehouses.models import Warehouse


# Create your models here.
class Bid(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='bids')
    status = models.CharField(max_length=244, default="yuborilgan")
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
    status = models.CharField(max_length=244, default="yuborilgan")
    # description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='bidInWarehouses', null=True, blank=True)

    def __str__(self) -> str:
        return str(self.object.name)


class BidProductToWarehouse(models.Model):
    product = models.ForeignKey(TemplateProduct, on_delete=models.CASCADE)
    amount = models.IntegerField()

    bid = models.ForeignKey(BidToWarehouse, on_delete=models.CASCADE, related_name='products')

    def __str__(self) -> str:
        return str(self.product.name)


class ObjectProductBase(models.Model):
    product = models.ForeignKey(TemplateProduct, on_delete=models.CASCADE, related_name='object_products_base',
                                null=True)
    amount = models.IntegerField(default=0)
    total_price = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='object_products_base', null=True,
                               blank=True)

    def __str__(self) -> str:
        return f"{self.product.name}"


class ObjectProducts(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    size = models.CharField(max_length=50)
    price = models.CharField(max_length=155, null=True, blank=True)
    total_price = models.CharField(max_length=255, null=True, blank=True)

    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='object_products', null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='object_products', null=True,
                                  blank=True)

    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='object_products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)
