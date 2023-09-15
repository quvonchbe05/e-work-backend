from django.shortcuts import render
from .models import Bid, BidProduct, BidToWarehouse, BidProductToWarehouse
from .serializers import BidCreateSerializer, BidListSerializer
from products.models import TemplateProduct
from objects.models import Object
from accounts.models import CustomUser
from products.models import ProductBase
from objects.models import Object
from warehouses.models import Warehouse
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.utils import decode_jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import json


# Create your views here.
class CreateBidForM(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

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

            return Response(
                status=201, data={"status": "success", "bid_id": new_bid.pk}
            )

        else:
            return Response(status=400, data={"error": serializer.errors})


class BidMyList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = decode_jwt(request)
        if not token:
            return Response(status=404, data={"error": "invalid token"})
        user = CustomUser.objects.filter(id=token["user_id"]).first()
        if not user:
            return Response(status=404, data={"error": "invalid token"})

        object = Object.objects.filter(worker__pk=user.pk).first()
        if not object:
            return Response(status=404, data={"error": "obyekt topilmadi"})

        bid = Bid.objects.filter(object__pk=object.pk)
        bid_arr = []

        for b in bid:
            bid_arr.append(
                {
                    "id": b.pk,
                    "status": b.status,
                    "description": b.description,
                    "created_at": b.created_at,
                    "products": [],
                }
            )

        for b in bid_arr:
            products = BidProduct.objects.filter(bid__pk=b["id"])
            for p in products:
                b["products"].append(
                    {"id": p.pk, "name": p.product.name, "amount": p.amount}
                )

        return Response(status=200, data=bid_arr)


class GetBidById(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        bid = Bid.objects.filter(pk=pk).first()

        if not bid:
            return Response(status=404, data={"error": "Zayavka topilmadi!"})

        bid_obj = {
            "id": bid.pk,
            "object": bid.object.name,
            "worker": bid.object.worker.name,
            "phone": bid.object.worker.phone,
            "status": bid.status,
            "description": bid.description,
            "created_at": bid.created_at,
            "products": [],
        }
        products = BidProduct.objects.filter(bid__pk=bid.pk)
        for p in products:
            bid_obj["products"].append(
                {
                    "id": p.product.pk,
                    "name": p.product.name,
                    "amount": p.amount,
                    "size": p.product.size,
                }
            )

        return Response(status=200, data=bid_obj)


class BidList(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        bid = Bid.objects.all()
        bid_arr = []

        for b in bid:
            bid_arr.append(
                {
                    "id": b.pk,
                    "status": b.status,
                    "description": b.description,
                    "created_at": b.created_at,
                }
            )

        for b in bid_arr:
            products = BidProduct.objects.filter(bid__pk=b["id"])
            for p in products:
                b["products"].append(
                    {"id": p.pk, "name": p.product.name, "amount": p.amount}
                )

        return Response(status=200, data=bid_arr)


class ComparisonBidById(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        bid = Bid.objects.filter(pk=pk).first()

        if not bid:
            return Response(status=404, data={"error": "Zayavka topilmadi!"})

        bid_products = BidProduct.objects.filter(bid=bid.pk)
        products_response = []

        for bp in bid_products:
            products = ProductBase.objects.filter(product__pk=bp.product.pk)
            old_product = []
            for p in products:
                if bp.amount <= p.amount:
                    filtered_product = list(
                        filter(lambda obj: obj["id"] == p.product.pk, products_response)
                    )
                    if not filtered_product:
                        products_response.append(
                            {
                                "id": p.product.pk,
                                "name": p.product.name,
                                "size": p.product.size,
                                "amount": p.amount,
                                "price": p.product.amount,
                                "warehouse": {
                                    "id": p.warehouse.pk,
                                    "name": p.warehouse.name,
                                    "address": p.warehouse.address,
                                    "phone": p.warehouse.worker.phone,
                                    "worker": p.warehouse.worker.name,
                                },
                            }
                        )
                else:
                    old_product.append(p)
                    total_amount = sum([obj.amount for obj in old_product])
                    for op in old_product:
                        if bp.amount <= total_amount:
                            products_response.append(
                                {
                                    "id": op.product.pk,
                                    "name": op.product.name,
                                    "size": op.product.size,
                                    "amount": op.amount,
                                    "price": op.product.amount,
                                    "warehouse": {
                                        "id": op.warehouse.pk,
                                        "name": op.warehouse.name,
                                        "address": op.warehouse.address,
                                        "phone": op.warehouse.worker.phone,
                                        "worker": op.warehouse.worker.name,
                                    },
                                }
                            )

        return Response(status=200, data=products_response)


class CreateBidToWarehouse(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        bid = Bid.objects.filter(pk=pk).first()

        if not bid:
            return Response(status=404, data={"error": "Zayavka topilmadi!"})

        # new_bid_to_warehoue = BidToWarehouse(object=object, warehouse=request.data['warehouse'], description=request.data["description"])
        # new_bid_to_warehoue.save()

        bid_products = BidProduct.objects.filter(bid=bid.pk)
        products_response = []

        for bp in bid_products:
            products = ProductBase.objects.filter(product__pk=bp.product.pk)
            old_product = []
            for p in products:
                if bp.amount <= p.amount:
                    filtered_product = list(
                        filter(lambda obj: obj["id"] == p.product.pk, products_response)
                    )
                    if not filtered_product:
                        products_response.append(
                            {
                                "id": p.product.pk,
                                "name": p.product.name,
                                "size": p.product.size,
                                "amount": p.amount,
                                "price": p.product.amount,
                                "warehouse": {
                                    "id": p.warehouse.pk,
                                    "name": p.warehouse.name,
                                    "address": p.warehouse.address,
                                    "phone": p.warehouse.worker.phone,
                                    "worker": p.warehouse.worker.name,
                                },
                            }
                        )
                else:
                    old_product.append(p)
                    total_amount = sum([obj.amount for obj in old_product])
                    for op in old_product:
                        if bp.amount <= total_amount:
                            products_response.append(
                                {
                                    "id": op.product.pk,
                                    "name": op.product.name,
                                    "size": op.product.size,
                                    "amount": op.amount,
                                    "price": op.product.amount,
                                    "warehouse": {
                                        "id": op.warehouse.pk,
                                        "name": op.warehouse.name,
                                        "address": op.warehouse.address,
                                        "phone": op.warehouse.worker.phone,
                                        "worker": op.warehouse.worker.name,
                                    },
                                }
                            )

        test_response = [
            {
                "id": 25,
                "name": "Oxak",
                "size": "kg",
                "amount": 1400,
                "price": 1,
                "warehouse": {
                    "id": 14,
                    "name": "1-ombor",
                    "address": "Chilonzor 12kv",
                    "phone": "998908081791",
                    "worker": "Shodiyor",
                },
            },
            {
                "id": 21,
                "name": "Qum",
                "size": "tonna",
                "amount": 107,
                "price": 1,
                "warehouse": {
                    "id": 16,
                    "name": "3-ombor",
                    "address": "Olmozor tumani 2kv",
                    "phone": "998901292221",
                    "worker": "Raximov Sanjar",
                },
            },
            {
                "id": 23,
                "name": "Armatura",
                "size": "metr",
                "amount": 997,
                "price": 1,
                "warehouse": {
                    "id": 14,
                    "name": "1-ombor",
                    "address": "Chilonzor 12kv",
                    "phone": "998908081791",
                    "worker": "Shodiyor",
                },
            },
            {
                "id": 23,
                "name": "Armatura",
                "size": "metr",
                "amount": 971,
                "price": 1,
                "warehouse": {
                    "id": 16,
                    "name": "3-ombor",
                    "address": "Olmozor tumani 2kv",
                    "phone": "998901292221",
                    "worker": "Raximov Sanjar",
                },
            },
        ]

        filtered_products_with_warehouse = list(
            set(
                json.dumps(json_object["warehouse"])
                for json_object in products_response
            )
        )

        fpwwj = [
            json.loads(json_object) for json_object in filtered_products_with_warehouse
        ]

        for fpr in fpwwj:
            object = Object.objects.filter(pk=bid.object.pk).first()
            warehouse = Warehouse.objects.filter(pk=fpr["id"]).first()
            new_bid_to_warehouse = BidToWarehouse(object=object, warehouse=warehouse)
            new_bid_to_warehouse.save()

            for pr in products_response:
                if pr["warehouse"]["id"] == fpr["id"]:
                    product = TemplateProduct.objects.filter(pk=p["product"]).first()
                    if not product:
                        return Response(
                            status=404,
                            data={
                                "error": f"{p['name']}`ning id`si notog'ri kiritildi va maxsulot topilmadi!"
                            },
                        )

                    new_bid_product = BidProductToWarehouse(
                        product=product, amount=p["amount"], bid=new_bid_to_warehouse
                    )
                    new_bid_product.save()

        return Response(
            status=200,
            data={"status": "success", "bid_id": new_bid_to_warehouse.pk},
        )
