from django.shortcuts import render
from .models import Bid, BidProduct, BidToWarehouse, BidProductToWarehouse
from .serializers import (
    BidCreateSerializer,
    BidListSerializer,
    BidToWarehouseSerializer,
)
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
            "object_id": bid.object.pk,
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
                    "objects": [],
                }
            )

        for bp in bid_obj["products"]:
            products = ProductBase.objects.filter(product__pk=bp['id'])
            old_product = []
            for p in products:
                if bp['amount'] <= p.amount:
                    filtered_product = list(
                        filter(lambda obj: obj["id"] == p.product.pk, bp['objects'])
                    )
                    if not filtered_product:
                        bp['objects'].append(
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
                        if bp['amount'] <= total_amount:
                            bp['objects'].append(
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
                    "products": [],
                    "object": {
                        "id": b.object.pk,
                        "name": b.object.name,
                        "address": b.object.address,
                        "phone": b.object.worker.phone,
                        "worker": b.object.worker.name,
                    },
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
    @swagger_auto_schema(request_body=BidToWarehouseSerializer)
    def post(self, request):
        serializer = BidToWarehouseSerializer(data=request.data)
        if serializer.is_valid():
            object_id = request.data["object_id"]
            bid_id = request.data["bid_id"]
            products = request.data["products"]

            object = Object.objects.filter(pk=object_id).first()
            if not object:
                return Response(status=404, data={"error": "Obyekt topilmadi"})

            bid = Bid.objects.filter(pk=bid_id).first()
            if not bid:
                return Response(status=404, data={"error": "Zayavka topilmadi"})

            unique_warehouses = list(set(p["warehouse_id"] for p in products))

            for id in unique_warehouses:
                warehouse = Warehouse.objects.filter(pk=id).first()
                if not warehouse:
                    return Response(status=404, data={"error": "Sklad topilmadi"})
                new_bid = BidToWarehouse(
                    object=object,
                    warehouse=warehouse,
                )
                new_bid.save()
                if not warehouse:
                    return Response(status=404, data={"error": "Sklad topilmadi"})

                request_products = list(
                    filter(lambda obj: obj["warehouse_id"] == id, products)
                )
                for p in request_products:
                    base_product = ProductBase.objects.filter(
                        pk=p["product_id"]
                    ).first()
                    if not base_product:
                        return Response(status=404, data={"error": "Produkt topilmadi"})

                    new_bid_product = BidProductToWarehouse(
                        product=base_product,
                        amount=p["amount"],
                        bid=new_bid,
                    )
                    new_bid_product.save()

                bid.status = "tasdiqlandi"
                bid.save()

        else:
            return Response(status=400, data={"errors": serializer.errors})

        return Response(
            status=200,
            data={"status": "success"},
        )


class CancelBid(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        bid = Bid.objects.filter(pk=pk).first()
        if not bid:
            return Response(status=404, data={"error": "Zayavka topilmadi!"})

        bid.status = "qaytarildi"
        bid.save()

        return Response(status=200, data={"status": "success"})


class ConfirmInWarehouse(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        token = decode_jwt(request)
        if not token:
            return Response(status=404, data={"error": "invalid token"})
        user = CustomUser.objects.filter(id=token["user_id"]).first()
        if not user:
            return Response(status=404, data={"error": "invalid token"})

        bid = BidToWarehouse.objects.filter(
            pk=pk, warehouse__worker__id=user.pk
        ).first()
        if not bid:
            return Response(status=404, data={"error": "Zayavka topilmadi!"})

        bid_products = BidProductToWarehouse.objects.filter(bid__id=bid.pk)

        for bp in bid_products:
            base_product = ProductBase.objects.filter(
                pk=bp.product.pk, warehouse__id=bid.warehouse.pk
            ).first()
            if not base_product:
                return Response(status=404, data={"error": "Base product not found"})

            base_product.amount = base_product.amount - bp.amount
            base_product.save()

        bid.status = "tasdiqlandi"
        bid.save()

        return Response(status=200, data={"status": "success"})


class BidToWarehouseList(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        token = decode_jwt(request)
        if not token:
            return Response(status=404, data={"error": "invalid token"})
        user = CustomUser.objects.filter(id=token["user_id"]).first()
        if not user:
            return Response(status=404, data={"error": "invalid token"})

        bid = BidToWarehouse.objects.filter(warehouse__worker__id=user.pk).first()
        bid_arr = []

        for b in bid:
            bid_arr.append(
                {
                    "id": b.pk,
                    "status": b.status,
                    "created_at": b.created_at,
                    "products": [],
                    "object": {
                        "id": b.object.pk,
                        "name": b.object.name,
                        "address": b.object.address,
                        "phone": b.object.worker.phone,
                        "worker": b.object.worker.name,
                    },
                }
            )

        for b in bid_arr:
            products = BidProductToWarehouse.objects.filter(bid__pk=b["id"])
            for p in products:
                b["products"].append(
                    {"id": p.pk, "name": p.product.name, "amount": p.amount}
                )

        return Response(status=200, data=bid_arr)
