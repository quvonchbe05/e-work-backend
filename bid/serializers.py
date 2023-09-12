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