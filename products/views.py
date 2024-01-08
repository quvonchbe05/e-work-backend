import io
from datetime import datetime, date, timedelta

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from fpdf import FPDF
from requests import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import CustomUser
from accounts.utils import decode_jwt
from bid.models import ObjectProducts
from objects.models import Object
from warehouses.models import Warehouse
from .models import Product, Delivery, TemplateProduct, ProductBase
from .models import ProductSet
from .serializers import (
    OrderSerializer,
    ProductListSerializer,
    ProductFirstCreateSerializer,
    ProductTemplateEditSerializer,
    MonitoringSerializer,
    WarehousesMonitoringSerializer,
    ProductTemplateHistorySerializer, ProductSetSerializer, ProductSetListSerializer)


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
            # token = 8
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = decode_jwt(request)
        # token = 8
        user = CustomUser.objects.filter(pk=token["user_id"]).first()
        warehouse = Warehouse.objects.filter(worker=user.pk).first()
        incoming = ProductBase.objects.filter(warehouse__id=warehouse.pk)
        incoming_products = set_to_s_admin_list(incoming)

        return Response(
            status=200,
            data=incoming_products,
        )


class ProductOutgoing(APIView):
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
            # token = 8
            if token:
                user = CustomUser.objects.filter(pk=token["user_id"]).first()

                warehouse = Warehouse.objects.filter(worker=user.pk).first()

                for product in products:
                    old_product = ProductBase.objects.filter(
                        product__id=product["product_id"],
                        warehouse__id=warehouse.pk
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
                                    data={"error": f"{old_product.product.name} soni yetarli emas!"},
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        incoming = ProductBase.objects.filter(warehouse__id=pk)
        incoming_products = set_to_s_admin_list(incoming)

        return Response(
            status=200,
            data=incoming_products,
        )


class ProductTemplateEdit(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TemplateProduct.objects.filter(status=True)
    serializer_class = ProductTemplateEditSerializer


class ProductTemplateHistory(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # queryset = TemplateProduct.objects.filter(status=True)
    # serializer_class = ProductTemplateHistorySerializer
    def get(self, request, pk):
        template_products = TemplateProduct.objects.filter(pk=pk).first()
        if template_products:
            serializer = ProductTemplateHistorySerializer(template_products)
            return Response(status=200, data=serializer.data)
        else:
            return Response(status=404, data="not found!")


class ProductTemplateDetail(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=MonitoringSerializer)
    def post(self, request):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)
        month = f"{date.today() + timedelta(days=1)}"[:7]
        year = date.today().year

        today_inthis = datetime.now()
        seven_days_ago = today - timedelta(days=7)

        warehouse_id = None
        if request.data["warehouse_id"] != "all":
            warehouse_id = request.data["warehouse_id"]
        else:
            warehouse_id = ""

        product_id = None
        template_product = None
        template_product_name = None
        if request.data["product_id"] != "all":
            product_id = request.data["product_id"]
            template_product = TemplateProduct.objects.filter(pk=int(product_id)).first()
            template_product_name = template_product.name
        else:
            product_id = ""
            template_product_name = ""

        object_id = None
        if request.data["object_id"] != "all":
            object_id = request.data["object_id"]
        else:
            object_id = ""

        status = None
        if request.data["status"] != "all":
            if request.data["status"] == "1":
                status = True
            elif request.data["status"] == "0":
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
                created_at__range=(seven_days_ago, tomorrow),
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

        products_arr = []
        kelgan_summa = 0
        ketgan_summa = 0

        objects = Object.objects.filter(pk__icontains=object_id)
        object_res = []
        for obj in objects:
            if request.data["date_id"] == "1":
                object_products = ObjectProducts.objects.filter(name__icontains=template_product_name,
                                                                object__pk__icontains=obj.pk,
                                                                created_at__icontains=today)
            elif request.data["date_id"] == "1":
                object_products = ObjectProducts.objects.filter(name__icontains=template_product_name,
                                                                object__pk__icontains=obj.pk,
                                                                created_at__icontains=yesterday)
            elif request.data["date_id"] == "1":
                object_products = ObjectProducts.objects.filter(name__icontains=template_product_name,
                                                                object__pk__icontains=obj.pk,
                                                                created_at__range=(seven_days_ago, tomorrow))
            elif request.data["date_id"] == "4":
                object_products = ObjectProducts.objects.filter(name__icontains=template_product_name,
                                                                object__pk__icontains=obj.pk,
                                                                created_at__icontains=month)
            else:
                object_products = ObjectProducts.objects.filter(name__icontains=template_product_name,
                                                                object__pk__icontains=obj.pk)

            p_summa = 0

            for p in object_products:
                p_summa += int(p.total_price)

            object_res.append({
                'name': obj.name,
                'summa': p_summa,
                'product_amount': len(object_products)
            })

        for product in products:
            if product.delivery.status == True:
                kelgan_summa += int(product.total_price)
            else:
                ketgan_summa += int(product.total_price)

            products_arr.append(
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

        return Response(
            status=200,
            data={
                "products": products_arr,
                'objects': object_res,
                "kelgan_summa": kelgan_summa,
                "ketgan_summa": ketgan_summa,
            },
        )


class WarehousesMonitoring(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Warehouse.objects.all()
    serializer_class = WarehousesMonitoringSerializer


class MonitoringChart(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=MonitoringSerializer)
    def post(self, request):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)
        month = f"{date.today() + timedelta(days=1)}"[:7]
        year = date.today().year

        today_inthis = datetime.now()
        seven_days_ago = today - timedelta(days=7)

        warehouse_id = None
        if request.data["warehouse_id"] != "all":
            warehouse_id = request.data["warehouse_id"]
        else:
            warehouse_id = ""

        product_id = None
        if request.data["product_id"] != "all":
            product_id = request.data["product_id"]
        else:
            product_id = ""

        status = None
        if request.data["status"] != "all":
            if request.data["status"] == "1":
                status = True
            elif request.data["status"] == "0":
                status = False
        else:
            status = ""

        # Logic

        warehouses = Warehouse.objects.filter(pk__icontains=warehouse_id)

        datasets = []
        labels = []

        for w in warehouses:

            if request.data["date_id"] == "1":
                all_products = Product.objects.filter(created_at__icontains=today)
                products = Product.objects.filter(
                    created_at__icontains=today,
                    warehouse__id__icontains=w.pk,
                    product__id__icontains=product_id,
                    delivery__status__icontains=status,
                )
            elif request.data["date_id"] == "2":
                all_products = Product.objects.filter(created_at__icontains=yesterday)
                products = Product.objects.filter(
                    created_at__icontains=yesterday,
                    warehouse__id__icontains=w.pk,
                    product__id__icontains=product_id,
                    delivery__status__icontains=status,
                )
            elif request.data["date_id"] == "3":
                all_products = Product.objects.filter(
                    created_at__range=(seven_days_ago, tomorrow),
                )
                products = Product.objects.filter(
                    created_at__range=(seven_days_ago, tomorrow),
                    warehouse__id__icontains=w.pk,
                    product__id__icontains=product_id,
                    delivery__status__icontains=status,
                )
            elif request.data["date_id"] == "4":
                all_products = Product.objects.filter(created_at__icontains=month)
                products = Product.objects.filter(
                    created_at__icontains=month,
                    warehouse__id__icontains=w.pk,
                    product__id__icontains=product_id,
                    delivery__status__icontains=status,
                )
            else:
                all_products = Product.objects.all()
                products = Product.objects.filter(
                    warehouse__id__icontains=w.pk,
                    product__id__icontains=product_id,
                    delivery__status__icontains=status,
                )

            pr = len(products) * 100
            if len(all_products) != 0:
                labels.append(w.name)
                foiz = round(pr / len(all_products))
                datasets.append(foiz)

        return Response(
            status=200,
            data={
                "labels": labels,
                "datasets": [
                    {
                        "data": datasets,
                        "backgroundColor": [
                            "rgba(255, 99, 132, 0.2)",
                            "rgba(54, 162, 235, 0.2)",
                            "rgba(255, 206, 86, 0.2)",
                            "rgba(75, 192, 192, 0.2)",
                            "rgba(153, 102, 255, 0.2)",
                            "rgba(255, 159, 64, 0.2)",
                        ],
                        "borderColor": [
                            "rgba(255, 99, 132, 1)",
                            "rgba(54, 162, 235, 1)",
                            "rgba(255, 206, 86, 1)",
                            "rgba(75, 192, 192, 1)",
                            "rgba(153, 102, 255, 1)",
                            "rgba(255, 159, 64, 1)",
                        ],
                        "borderWidth": 2,
                    },
                ],
            },
        )


class MonitoringLineChart(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=MonitoringSerializer)
    def post(self, request):
        today = date.today()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)
        month = f"{date.today() + timedelta(days=1)}"[:7]
        year = date.today().year

        today_inthis = datetime.now()
        seven_days_ago = today - timedelta(days=7)

        warehouse_id = None
        if request.data["warehouse_id"] != "all":
            warehouse_id = request.data["warehouse_id"]
        else:
            warehouse_id = ""

        product_id = None
        if request.data["product_id"] != "all":
            product_id = request.data["product_id"]
        else:
            product_id = ""

        status = None
        if request.data["status"] != "all":
            if request.data["status"] == "1":
                status = True
            elif request.data["status"] == "0":
                status = False
        else:
            status = ""

        # Logic
        if request.data["date_id"] == "1":
            product_dates = Product.objects.filter(
                created_at__icontains=today,
                warehouse__id__icontains=warehouse_id,
                product__id__icontains=product_id,
            )
        elif request.data["date_id"] == "2":
            product_dates = Product.objects.filter(
                created_at__icontains=yesterday,
                warehouse__id__icontains=warehouse_id,
                product__id__icontains=product_id,
            )
        elif request.data["date_id"] == "3":
            product_dates = Product.objects.filter(
                created_at__range=(seven_days_ago, tomorrow),
                warehouse__id__icontains=warehouse_id,
                product__id__icontains=product_id,
            )
        elif request.data["date_id"] == "4":
            product_dates = Product.objects.filter(
                created_at__icontains=month,
                warehouse__id__icontains=warehouse_id,
                product__id__icontains=product_id,
            )
        else:
            product_dates = Product.objects.filter(
                warehouse__id__icontains=warehouse_id,
                product__id__icontains=product_id,
                delivery__status__icontains=status,
            )

        products_arr = []

        unique_data = []
        dateSet = set()
        for pr in product_dates:
            created_at = pr.created_at.date()
            if created_at not in dateSet:
                unique_data.append(created_at)
                dateSet.add(created_at)

        for d in unique_data:
            ketgan_summa = Product.objects.filter(
                created_at__icontains=d, delivery__status=False, product__id__icontains=product_id,
            )
            ketgan_total_price = 0
            for ketgan in ketgan_summa:
                if status == False:
                    ketgan_total_price += int(ketgan.total_price)
                elif status == "":
                    ketgan_total_price += int(ketgan.total_price)
                else:
                    ketgan_total_price = 0

            kelgan_summa = Product.objects.filter(
                created_at__icontains=d, delivery__status=True, product__id__icontains=product_id,
            )
            kelgan_total_price = 0
            for kelgan in kelgan_summa:
                if status == True:
                    kelgan_total_price += int(kelgan.total_price)
                elif status == "":
                    kelgan_total_price += int(kelgan.total_price)
                else:
                    kelgan_total_price = 0

            products_arr.append(
                {"date": d, "ketgan": ketgan_total_price, "kelgan": kelgan_total_price}
            )

        return Response(products_arr)


class CreateProductSetView(APIView):

    @swagger_auto_schema(request_body=ProductSetSerializer)
    def post(self, request):
        serializer = ProductSetSerializer(data=request.data)

        if serializer.is_valid():
            object_id = serializer.validated_data["object_id"]
            obj = Object.objects.get(pk=object_id)

            product_set_data = {
                "data_array": serializer.validated_data["data_array"],
                "total_price": serializer.validated_data["total_price"],
                "object_id": obj,
            }
            ProductSet.objects.create(**product_set_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductSetDetailApi(APIView):

    def get(self, request, pk):
        obj = Object.objects.filter(pk=pk).first()
        if not obj:
            return Response(status=404, data={'error': 'Object not found'})

        productsets = obj.productset.all()

        if not productsets:
            return Response(status=404, data={'error': 'ProductSets not found for this Object'})

        productset_data = []
        for productset in productsets:
            productset_data.append({
                'id': productset.pk,
                'total_price': productset.total_price,
                'data_array': productset.data_array
            })
        total_price_sum = productsets.aggregate(Sum('total_price'))['total_price__sum'] or 0
        obj_json = {
            'id': obj.pk,
            'name': obj.name,
            'address': obj.address,
            'productsets': productset_data,
            'total_price': total_price_sum,
        }

        return Response(status=200, data=obj_json)


class ProductSetListAPi(ListAPIView):
    queryset = ProductSet.objects.all()
    serializer_class = ProductSetListSerializer


class ExportProductsAPI(APIView):
    def get(self, request, pk):
        obj = get_object_or_404(Object, pk=pk)
        try:
            projectset = ProductSet.objects.filter(object_id=obj)
            serializer = ProductSetListSerializer(projectset, many=True)
        except ProductSet.DoesNotExist:
            return Response(data={"error": "No productset found for this object"}, status=status.HTTP_404_NOT_FOUND)

        pdf = FPDF()

        for item in serializer.data:
            branch_name = item['data_array'][0]['name']
            total_price = item['total_price']
            products = item['data_array'][0]['products']

            pdf.add_page()  # Add a page for each branch

            pdf.set_font("Arial", 'B', 11)  # Set font and size for the table

            pdf.set_fill_color(200, 220, 255)  # Set the background color for header cells

            col_width = [60, 40, 20, 20, 30, 50]  # Adjust column widths as needed

            # First table for branch name
            pdf.cell(col_width[0], 10, "Branch Name", 0, 0, 'L', fill=True)
            pdf.cell(col_width[-1], 10, branch_name, 0, 1, 'C', fill=True)

            # Second table for product details
            pdf.cell(col_width[0], 10, "Product Name", 1)
            pdf.cell(col_width[1], 10, "Size", 1)
            pdf.cell(col_width[2], 10, "Count", 1)
            pdf.cell(col_width[3], 10, "Price", 1)
            pdf.cell(col_width[4], 10, "Total Price", 1)
            pdf.ln()

            for product in products:
                pdf.cell(col_width[0], 10, product['name'], 1)
                pdf.cell(col_width[1], 10, product['size'], 1)
                pdf.cell(col_width[2], 10, product['amount'], 1)
                pdf.cell(col_width[3], 10, product['price'], 1)
                pdf.cell(col_width[4], 10, str(float(product['price']) * float(product['amount'])), 1)
                pdf.ln()

            # Third table for branch total price
            pdf.cell(col_width[0], 10, "Total Price", 0, 0, 'L', fill=True)
            pdf.cell(col_width[-1], 10, str(total_price), 0, 1, 'C', fill=True)

        # Generate the PDF content as a string
        pdf_content = pdf.output(dest='S').encode('latin1')  # noqa

        response = FileResponse(io.BytesIO(pdf_content), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="output_{obj.pk}.pdf"'

        return response


class GetIncomingProductDeliveryAPi(APIView):

    def get(self, request):
        product_data = Product.objects.all().order_by('-created_at')[:5]
        result = []

        for product in product_data:
            if product.delivery.status == True:
                delivery_info = {
                    'name': product.delivery.name,
                    'phone': product.delivery.phone
                }

                try:
                    template_product = TemplateProduct.objects.get(pk=product.product_id)
                    productbase_info = {
                        'amount': product.amount,
                        'product_name': template_product.name,
                        'size': template_product.size,
                        'created_at': product.created_at
                    }
                    result.append({
                        'delivery_info': delivery_info,
                        'productbase_info': productbase_info
                    })
                except TemplateProduct.DoesNotExist:
                    template_product = None
        return Response(result)


class GetIncomingProductsDeliveryAPI(APIView):
    def get(self, request):
        product_data = Product.objects.filter(delivery__status=True).order_by('-created_at')[:5]
        result = self.get_product_info(product_data)
        return Response(result)

    def get_product_info(self, product_data):
        result = []

        for product in product_data:
            delivery_info = {
                'name': product.delivery.name,
                'phone': product.delivery.phone
            }

            template_product = get_object_or_404(TemplateProduct, pk=product.product_id)
            productbase_info = {
                'amount': product.amount,
                'product_name': template_product.name,
                'size': template_product.size,
                'created_at': product.created_at
            }

            result.append({
                'delivery_info': delivery_info,
                'productbase_info': productbase_info
            })

        return result


class GetOutgoingProductsDeliveryAPI(APIView):
    def get(self, request):
        product_data = Product.objects.filter(delivery__status=False).order_by('-created_at')[:5]
        result = self.get_product_info(product_data)
        return Response(result)

    def get_product_info(self, product_data):
        result = []

        for product in product_data:
            delivery_info = {
                'name': product.delivery.name,
                'phone': product.delivery.phone
            }

            template_product = get_object_or_404(TemplateProduct, pk=product.product_id)
            productbase_info = {
                'amount': product.amount,
                'product_name': template_product.name,
                'size': template_product.size,
                'created_at': product.created_at
            }

            result.append({
                'delivery_info': delivery_info,
                'productbase_info': productbase_info
            })

        return result
