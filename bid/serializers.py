from rest_framework import serializers
from .models import Bid

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    product = serializers.IntegerField()
    amount = serializers.IntegerField()
    class Meta:
        ref_name = 'product_in_bid'
    

class BidCreateSerializer(serializers.Serializer):
    products = serializers.ListSerializer(child=ProductSerializer())
    object = serializers.IntegerField()
    description = serializers.CharField(allow_null=True, allow_blank=True)


class BidListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('status', 'created_at')
        
        
class ProductForWarehouseSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    warehouse_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    class Meta:
        ref_name = 'product_in_bid_for_create'
        
class BidToWarehouseSerializer(serializers.Serializer):
    object_id = serializers.IntegerField()
    bid_id = serializers.IntegerField()
    products = serializers.ListSerializer(child=ProductForWarehouseSerializer())
    