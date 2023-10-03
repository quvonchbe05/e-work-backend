from rest_framework import serializers

from warehouses.models import Warehouse
from warehouses.serializers import UserForWarehouseSerializer
from .models import Delivery, TemplateProduct, ProductSet


class ProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    description = serializers.CharField(allow_null=True, allow_blank=True)


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


class ProductTemplateHistorySerializer(serializers.ModelSerializer):
    products_base = serializers.SerializerMethodField()

    def get_products_base(self, obj):
        return [
            {
                "id": p.id,
                "amount": p.amount,
                "total_price": p.total_price,
                "warehouse": {
                    "name": p.warehouse.name,
                    "address": p.warehouse.address
                },
            }
            for p in obj.products_base.all()
        ]

    class Meta:
        model = TemplateProduct
        fields = ("name", "size", "price", "products_base")


class MonitoringSerializer(serializers.Serializer):
    date_id = serializers.CharField()
    warehouse_id = serializers.CharField()
    object_id = serializers.CharField()
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


class ProductSetSerializer(serializers.Serializer):
    total_price = serializers.FloatField()
    data_array = serializers.ListField()
    object_id = serializers.IntegerField()


class ProductSetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSet
        fields = '__all__'

