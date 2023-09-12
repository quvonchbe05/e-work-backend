from rest_framework import serializers

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

