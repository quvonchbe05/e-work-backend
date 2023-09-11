from rest_framework import serializers
from .models import CustomUser
from warehouses.serializers import WarehouseSerializer
import json
from warehouses.models import Warehouse

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
        
        
class UserFirstEditSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True, read_only=False)
    password = serializers.CharField(required=False, allow_blank=True, allow_null=True, read_only=False, min_length=8)
    
    
class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    username = serializers.CharField()
    role = serializers.CharField()
    

class UserListSerializer(serializers.ModelSerializer):
    warehouse = serializers.SerializerMethodField()
    
    def get_warehouse(self, obj):
        whs = [{'name':wh.name,'address':wh.address} for wh in obj.warehouse.all()]
        if len(whs):
            return whs[0]
    
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'phone', 'username', 'warehouse', 'role')
        
        
        
class UserEditSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name', 'phone', 'username', 'role')