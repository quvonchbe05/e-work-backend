from rest_framework import serializers
from .models import Warehouse
from accounts.models import CustomUser

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        
        
class UserForWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'username', 'phone')
 
 
class WarehouseListSerializer(serializers.ModelSerializer):
    worker = UserForWarehouseSerializer()
    class Meta:
        model = Warehouse
        fields = ('id', 'name', 'address', 'worker')