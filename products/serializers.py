from rest_framework import serializers
from .models import Product, Delivery, TemplateProduct


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
        model = TemplateProduct
        fields = ('id', 'name', 'amount', 'size', 'price')
        
        
        
class ProductFirstCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateProduct
        fields = ('name', 'amount', 'size', 'price')
        

class ProductTemplateEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateProduct
        fields = '__all__'