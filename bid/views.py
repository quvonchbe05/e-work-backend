from django.shortcuts import render
from .models import Bid, BidProduct
from .serializers import BidCreateSerializer
from products.models import TemplateProduct
from objects.models import Object
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class CreateBitForM(APIView):
    @swagger_auto_schema(request_body=BidCreateSerializer)
    def post(self, request):
        
        serializer = BidCreateSerializer(data=request.data)

        if serializer.is_valid():
            object = Object.objects.filter(pk=request.data["object"]).first()
            if not object:
                return Response(status=404, data={"error": "Obyekt topilmadi"})

            new_bid = Bid(object=object, description=request.data["description"])
            new_bid.save()

            for p in request.data["products"]:
                product = TemplateProduct.objects.filter(pk=p["product"]).first()
                if not product:
                    return Response(
                        status=404,
                        data={
                            "error": f"{p['name']}`ning id`si notog'ri kiritildi va maxsulot topilmadi!"
                        },
                    )

                new_bid_product = BidProduct(
                    product=product, amount=p["amount"], bid=new_bid
                )
                new_bid_product.save()

            return Response(status=201, data={"status": "success"})

        else:
            return Response(status=400, data={"error": serializer.errors})
