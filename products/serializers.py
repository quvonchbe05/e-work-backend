from rest_framework import serializers
from .models import Product, Delivery


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'amount', 'size', 'description')
        
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('name', 'phone', 'status')

class OrderSerializer(serializers.Serializer):
    products = serializers.ListSerializer(child=ProductSerializer())
    delivery = DeliverySerializer()


