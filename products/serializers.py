from rest_framework import serializers
from .models import Product, Delivery, TemplateProduct
import json
from warehouses.models import Warehouse
from warehouses.serializers import UserForWarehouseSerializer


class ProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    description = serializers.CharField()


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ("name", "phone")


class OrderSerializer(serializers.Serializer):
    products = serializers.ListSerializer(child=ProductSerializer())
    delivery = DeliverySerializer()
    status = serializers.BooleanField()


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateProduct
        fields = ("id", "name", "amount", "size", "price")


class ProductFirstCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateProduct
        fields = ("name", "amount", "size", "price")


class ProductTemplateEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateProduct
        fields = ("name", "amount", "size", "price")


class MonitoringSerializer(serializers.Serializer):
    date_id = serializers.CharField()
    warehouse_id = serializers.CharField()
    product_id = serializers.CharField()
    status = serializers.BooleanField()


class WarehousesMonitoringSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    worker = UserForWarehouseSerializer()

    def get_products(self, obj):
        return [
            {
                "id": p.id,
                "name": p.product.name,
                "amount": p.amount,
                "price": p.product.price,
                "size": p.product.size,
                "total_price": p.total_price,
                "status": p.delivery.status,
                "date": p.created_at,
                "delivery": {
                    "id": p.delivery.pk,
                    "name": p.delivery.name,
                    "phone": p.delivery.phone,
                },
            }
            for p in obj.products.all()
        ]

    class Meta:
        model = Warehouse
        fields = ("id", "name", "address", "worker", "products")
