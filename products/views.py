from django.shortcuts import render, get_object_or_404, get_list_or_404
from accounts.models import CustomUser
from .models import Product, Delivery, TemplateProduct, ProductBase
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
    ProductTemplateEditSerializer,
    MonitoringSerializer,
    WarehousesMonitoringSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.utils import decode_jwt
from datetime import datetime, date, timedelta
from warehouses.models import Warehouse


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
                    template_product = TemplateProduct.objects.filter(
                        pk=product["product_id"], status=True
                    ).first()

                    if template_product:
                        if warehouse:
                            product_base = ProductBase.objects.filter(
                                product=template_product, warehouse=warehouse
                            ).first()

                            if product_base:
                                product_base.amount += product["amount"]
                                product_base.total_price = (
                                    int(template_product.price) * product_base.amount
                                )
                                product_base.save()

                            else:
                                new_product_base = ProductBase(
                                    product=template_product,
                                    amount=product["amount"],
                                    warehouse=warehouse,
                                    total_price=int(template_product.price)
                                    * product["amount"],
                                )
                                new_product_base.save()

                            new_product = Product(
                                product=template_product,
                                amount=product["amount"],
                                description=product["description"],
                                delivery=new_delivery,
                                warehouse=warehouse,
                                total_price=int(template_product.price)
                                * product["amount"],
                            )

                            new_product.save()

                        else:
                            return Response(
                                status=404, data={"error": "Ombor topilmadi!"}
                            )
                    else:
                        return Response(
                            status=404, data={"error": "Maxsulot topilmadi!"}
                        )

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


class ProductList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TemplateProduct.objects.filter(status=True)
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
                "size": product.product.size,
                "total_price": product.total_price,
                "status": product.delivery.status,
                "date": product.created_at,
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


def set_to_s_admin_list(arr):
    all_products = []
    for product in arr:
        all_products.append(
            {
                "id": product.id,
                "name": product.product.name,
                "amount": product.amount,
                "price": product.product.price,
                "size": product.product.size,
                "total_price": product.total_price,
            }
        )
    return all_products


class ProductEditedList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all = Product.objects.all()
        incoming = Product.objects.filter(delivery__status=True)
        outgoing = Product.objects.filter(delivery__status=False)
        all_products = set_to_list(all)
        incoming_products = set_to_list(incoming)
        outgoing_products = set_to_list(outgoing)

        return Response(
            status=200,
            data={
                "all": all_products,
                "incoming": incoming_products,
                "outgoing": outgoing_products,
            },
        )


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

        return Response(
            status=200,
            data={
                "all": all_products,
                "incoming": incoming_products,
                "outgoing": outgoing_products,
            },
        )


class ProductOutgoingList(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        token = decode_jwt(request)
        user = CustomUser.objects.filter(pk=token["user_id"]).first()
        warehouse = Warehouse.objects.filter(worker=user.pk).first()
        incoming = ProductBase.objects.filter(warehouse__id=warehouse.pk)
        incoming_products = set_to_s_admin_list(incoming)

        return Response(
            status=200,
            data=incoming_products,
        )


class ProductOutgoing(APIView):
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
                    old_product = ProductBase.objects.filter(
                        pk=product["product_id"]
                    ).first()
                    if old_product:
                        template_product = TemplateProduct.objects.filter(
                            pk=old_product.product.pk, status=True
                        ).first()
                        if warehouse:
                            if old_product.amount > product["amount"]:
                                old_product.amount = (
                                    old_product.amount - product["amount"]
                                )
                                old_product.total_price = (
                                    int(template_product.price) * old_product.amount
                                )
                                old_product.save()

                                new_product = Product(
                                    product=template_product,
                                    amount=product["amount"],
                                    description=product["description"],
                                    delivery=new_delivery,
                                    warehouse=warehouse,
                                    total_price=int(template_product.price)
                                    * product["amount"],
                                )
                                new_product.save()

                            else:
                                return Response(
                                    status=404,
                                    data={"error": "Maxsulot soni yetarli emas!"},
                                )
                        else:
                            return Response(
                                status=404, data={"error": "Ombor topilmadi!"}
                            )
                    else:
                        return Response(
                            status=404, data={"error": "Maxsulot topilmadi!"}
                        )

                return Response(status=201, data={"staus": "success"})
            else:
                return Response(status=400, data={"error": "Token mavjud emas"})
        else:
            return Response(status=400, data={"error": seralizer.errors})


class ProductWarehouseHistoryList(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        token = decode_jwt(request)
        user = CustomUser.objects.filter(pk=token["user_id"]).first()
        warehouse = Warehouse.objects.filter(worker=user.pk).first()

        incoming = Product.objects.filter(warehouse__id=warehouse.pk)
        incoming_products = set_to_list(incoming)

        return Response(
            status=200,
            data=incoming_products,
        )


class ProductWarehouseAllList(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        incoming = ProductBase.objects.filter(warehouse__id=pk)
        incoming_products = set_to_s_admin_list(incoming)

        return Response(
            status=200,
            data=incoming_products,
        )


class ProductTemplateEdit(generics.UpdateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = TemplateProduct.objects.filter(status=True)
    serializer_class = ProductTemplateEditSerializer


class ProductTemplateDetail(generics.RetrieveAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = TemplateProduct.objects.filter(status=True)
    serializer_class = ProductListSerializer


class PRoductTemplateDelete(APIView):
    def delete(self, request, pk):
        product = TemplateProduct.objects.filter(status=True, pk=pk).first()
        if product:
            product.status = False
            product.save()
            return Response(status=200, data={"status": "success"})
        else:
            return Response(status=404, data="Product topilmadi")


class Monitoring(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=MonitoringSerializer)
    def post(self, request):
        today = date.today()
        yesterday = today - timedelta(days=1)
        month = f"{date.today()}"[:7]
        year = date.today().year

        today_inthis = datetime.now()
        seven_days_ago = today - timedelta(days=7)
        
        warehouse_id = None
        if request.data['warehouse_id'] != "all":
            warehouse_id = request.data['warehouse_id']
        else:
            warehouse_id = ""
        
        product_id = None
        if request.data['product_id'] != "all":
            product_id = request.data['product_id']
        else:
            product_id = ""
        
        status = None
        if request.data['status'] != "all":
            if request.data['status'] == "1":
                status = True
            elif request.data['status'] == "0":
                status = False
        else:
            status = ""
        
        if request.data["date_id"] == "1":
            products = Product.objects.filter(
                created_at__icontains=today,
                warehouse__id__icontains=warehouse_id,
                product__id__icontains=product_id,
                delivery__status__icontains=status,
            )
        elif request.data["date_id"] == "2":
            products = Product.objects.filter(
                created_at__icontains=yesterday,
                warehouse__id__icontains=warehouse_id,
                product__id__icontains=product_id,
                delivery__status__icontains=status,
            )
        elif request.data["date_id"] == "3":
            products = Product.objects.filter(
                created_at__range=(seven_days_ago, today_inthis),
                warehouse__id__icontains=warehouse_id,
                product__id__icontains=product_id,
                delivery__status__icontains=status,
            )
        elif request.data["date_id"] == "4":
            products = Product.objects.filter(
                created_at__icontains=month,
                warehouse__id__icontains=warehouse_id,
                product__id__icontains=product_id,
                delivery__status__icontains=status,
            )
        else:
            products = Product.objects.filter(
                warehouse__id__icontains=warehouse_id,
                product__id__icontains=product_id,
                delivery__status__icontains=status,
            )

        products_arr = set_to_list(products)
        return Response(status=200, data=products_arr)



class WarehousesMonitoring(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Warehouse.objects.all()
    serializer_class = WarehousesMonitoringSerializer