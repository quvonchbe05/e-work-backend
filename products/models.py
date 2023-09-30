from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import CASCADE

from objects.models import Object
from warehouses.models import Warehouse


class ProductSet(models.Model):
    total_price = models.FloatField(null=True, blank=True)
    data_array = ArrayField(models.JSONField(), null=True, blank=True)
    object_id = models.ForeignKey(Object, on_delete=CASCADE, null=True, blank=True, related_name='productset')


class TemplateProduct(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    size = models.CharField(max_length=50)
    price = models.FloatField(null=True, blank=True)

    status = models.BooleanField(default=True)
    total_price = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Delivery(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    status = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.name}"


class Product(models.Model):
    product = models.ForeignKey(TemplateProduct, on_delete=models.CASCADE, related_name='products', null=True)
    amount = models.IntegerField(default=0)
    total_price = models.CharField(max_length=255, null=True, blank=True)

    date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.product.name}"


class ProductBase(models.Model):
    product = models.ForeignKey(TemplateProduct, on_delete=models.CASCADE, related_name='products_base', null=True)
    amount = models.IntegerField(default=0)
    total_price = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='products_base', null=True,
                                  blank=True)

    def __str__(self) -> str:
        return f"{self.product.name}"
