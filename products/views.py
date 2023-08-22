from django.shortcuts import render, get_object_or_404, get_list_or_404
from accounts.models import CustomUser
from .models import Product, Delivery
from warehouses.models import Warehouse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    OrderSerializer,
    ProductSerializer,
    DeliverySerializer,
    ProductListSerializer,
    ProductFirstCreateSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.utils import decode_jwt


# Create your views here.
class ProductSAdminEdit(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):
        seralizer = OrderSerializer(data=request.data)
        if seralizer.is_valid():
            products = request.data["products"]
            delivery = request.data["delivery"]
            status = request.data["status"]

            new_delivery = Delivery(
                name=delivery["name"],
                phone=delivery["phone"],
                status=status,
            )

            new_delivery.save()

            token = decode_jwt(request)
            if token:
                user = CustomUser.objects.filter(pk=token["user_id"]).first()
                warehouse = Warehouse.objects.filter(worker=user.pk).first()

                for product in products:
                    if warehouse:
                        new_product = get_object_or_404(
                            Product, pk=product["product_id"]
                        )
                        new_product.amount = product["amount"]
                        new_product.description = product["description"]
                        new_product.delivery = new_delivery
                        new_product.warehouse = warehouse
                        new_product.save()
                    else:
                        return Response(status=404, data={"error": "Ombor topilmadi!"})

                return Response(status=201, data={"staus": "success"})
            else:
                return Response(status=400, data={"error": "Token mavjud emas"})
        else:
            return Response(status=400, data={"error": seralizer.errors})


class ProductFirstCreate(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ProductFirstCreateSerializer)
    def post(self, request):
        serializer = ProductFirstCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_product = Product(
                name=request.data["name"],
                amount=request.data["amount"],
                size=request.data["size"],
                price=request.data["price"],
            )
            new_product.save()
            return Response(
                status=201,
                data={
                    "name": new_product.name,
                    "amount": new_product.amount,
                    "size": new_product.size,
                    "price": new_product.price,
                },
            )
        else:
            return Response(status=400, data={"error": serializer.errors})


class ProductSearchForS(APIView):
    def get(self, request, product_name):
        products = Product.objects.filter(name__icontains=product_name)
        products_json = []
        for product in products:
            products_json.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "amount": product.amount,
                    "size": product.size,
                    "price": product.price,
                }
            )
        return Response(status=200, data=products_json)


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class Units(APIView):
    def get(self, request):
        units = [
            {"id": 1, "abbreviation": "KG"},
            {"id": 2, "abbreviation": "TONNA"},
            {"id": 3, "abbreviation": "LITR"},
            {"id": 4, "abbreviation": "METR"},
            {"id": 5, "abbreviation": "SANTIMETR"},
            {"id": 6, "abbreviation": "DONA"},
        ]
        return Response(status=200, data=units)
