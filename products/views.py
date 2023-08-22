from django.shortcuts import render, get_object_or_404, get_list_or_404
from accounts.models import CustomUser
from .models import Product, Delivery, TemplateProduct
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
                    template_product = TemplateProduct.objects.filter(pk=product['product_id']).first()
                    if template_product:
                        if warehouse:
                            new_product = Product(
                                product = template_product,
                                amount = product["amount"],
                                description = product["description"],
                                delivery = new_delivery,
                                warehouse = warehouse,
                                total_price = (
                                    int(template_product.price) * product["amount"]
                                ),
                            )
                            new_product.save()
                        else:
                            return Response(status=404, data={"error": "Ombor topilmadi!"})
                    else:
                        return Response(status=404, data={"error": "Maxsulot topilmadi!"})

                return Response(status=201, data={"staus": "success"})
            else:
                return Response(status=400, data={"error": "Token mavjud emas"})
        else:
            return Response(status=400, data={"error": seralizer.errors})


class ProductFirstCreate(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TemplateProduct.objects.all()
    serializer_class = ProductFirstCreateSerializer
    


# class ProductSearchForS(APIView):
#     def get(self, request, product_name):
#         products = Product.objects.filter(name__icontains=product_name)
#         products_json = []
#         for product in products:
#             products_json.append(
#                 {
#                     "id": product.id,
#                     "name": product.name,
#                     "amount": product.amount,
#                     "size": product.size,
#                     "price": product.price,
#                 }
#             )
#         return Response(status=200, data=products_json)


class ProductList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TemplateProduct.objects.all()
    serializer_class = ProductListSerializer


class Units(APIView):
    def get(self, request):
        units = [
            {"id": 1, "abbreviation": "kg"},
            {"id": 2, "abbreviation": "tonna"},
            {"id": 3, "abbreviation": "litr"},
            {"id": 4, "abbreviation": "metr"},
            {"id": 5, "abbreviation": "sm"},
            {"id": 6, "abbreviation": "dona"},
        ]
        return Response(status=200, data=units)


def set_to_list(arr):
    all_products = []
    for product in arr:
        all_products.append(
            {
                "id": product.id,
                "name": product.product.name,
                "amount": product.amount,
                "price": product.product.price,
                "total_price": product.total_price,
                "delivery": {
                    "id": product.delivery.pk,
                    "name": product.delivery.name,
                    "phone": product.delivery.phone,
                },
                "warehouse": {
                    "id": product.warehouse.pk,
                    "name": product.warehouse.name,
                    "address": product.warehouse.address,
                },
            }
        )
    return all_products


class ProductEditedList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all = Product.objects.all()
        incoming = Product.objects.all(delivery__status=True)
        outgoing = Product.objects.all(delivery__status=False)
        all_products = set_to_list(all)
        incoming_products = set_to_list(incoming)
        outgoing_products = set_to_list(outgoing)

        return Response(status=200, data={
            "all": all_products,
            "incoming": incoming_products,
            "outgoing": outgoing_products,
        })



class ProductByWarehouseList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        all = Product.objects.filter(warehouse__id=pk)
        incoming = Product.objects.filter(delivery__status=True, warehouse__id=pk)
        outgoing = Product.objects.filter(delivery__status=False, warehouse__id=pk)
        all_products = set_to_list(all)
        incoming_products = set_to_list(incoming)
        outgoing_products = set_to_list(outgoing)

        return Response(status=200, data={
            "all": all_products,
            "incoming": incoming_products,
            "outgoing": outgoing_products,
        })
