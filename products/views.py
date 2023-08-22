from django.shortcuts import render
from .models import Product, Delivery
from warehouses.models import Warehouse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import OrderSerializer, ProductSerializer, DeliverySerializer


# Create your views here.
class ProductCreate(APIView):
    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):
        seralizer = OrderSerializer(data=request.data)
        if seralizer.is_valid():
            products = request.data["products"]
            delivery = request.data["delivery"]

            new_delivery = Delivery(
                name=delivery["name"],
                phone=delivery["phone"],
                status=delivery["status"],
            )

            new_delivery.save()

            for product in products:
                warehouse = Warehouse.objects.filter(pk=product["warehouse"]).first()
                if warehouse:
                    new_product = Product(
                        name=product["name"],
                        amount=product["amount"],
                        size=product["size"],
                        warehouse=warehouse,
                        description=product["description"],
                        delivery=new_delivery,
                    )
                    new_product.save()
                else:
                    return Response(status=404, data={"error": "Ombor topilmadi!"})

            return Response(status=201, data={"staus": "success"})
        else:
            return Response(status=400, data={'error': seralizer.errors})
