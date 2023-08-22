from rest_framework import serializers
from .models import Product, Delivery


class ProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    description = serializers.CharField()
        
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('name', 'phone')

class OrderSerializer(serializers.Serializer):
    products = serializers.ListSerializer(child=ProductSerializer())
    delivery = DeliverySerializer()
    status = serializers.BooleanField()



class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'amount', 'size', 'price')
        
        
        
class ProductFirstCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'amount', 'size', 'price')
        
