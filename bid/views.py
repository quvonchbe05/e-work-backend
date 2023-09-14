from django.shortcuts import render
from .models import Bid, BidProduct
from .serializers import BidCreateSerializer, BidListSerializer
from products.models import TemplateProduct
from objects.models import Object
from accounts.models import CustomUser
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.utils import decode_jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Create your views here.
class CreateBidForM(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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

            return Response(status=201, data={
                "status": "success",
                "bid_id": new_bid.pk
            })

        else:
            return Response(status=400, data={"error": serializer.errors})



class BidMyList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        token = decode_jwt(request)
        if not token:
            return Response(status=404, data={'error': "invalid token"})
        user = CustomUser.objects.filter(id=token['user_id']).first()
        if not user:
            return Response(status=404, data={'error': "invalid token"})
        
        
        object = Object.objects.filter(worker__pk=user.pk).first()
        if not object:
            return Response(status=404, data={'error': "obyekt topilmadi"})
        
        
        bid = Bid.objects.filter(object__pk=object.pk)
        bid_arr = []
        
        for b in bid:
            bid_arr.append({
                'id': b.pk,
                'status': b.status,
                'description': b.description,
                'created_at': b.created_at,
            })
        
            products = BidProduct.objects.filter(bid__pk=b.pk)
            for p in products:
                b['products'].append({
                    'id': p.pk,
                    'name': p.product.name,
                    'amount': p.amount
                })
        
        
        return Response(status=200, data=bid_arr)
    
    
    
class GetBidById(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        bid = Bid.objects.filter(pk=pk).first()
        
        if not bid:
            return Response(status=404, data={'error': "Zayavka topilmadi!"})

        bid_obj = {
            'id': bid.pk,
            'status': bid.status,
            'description': bid.description,
            'created_at': bid.created_at,
            'products': [],
        }
        products = BidProduct.objects.filter(bid__pk=bid.pk)
        for p in products:
            bid_obj['products'].append({
                'id': p.product.pk,
                'name': p.product.name,
                'amount': p.amount
            })
        
        
        return Response(status=200, data=bid_obj)
    
    
    
class BidList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        bid = Bid.objects.all()
        bid_arr = []
        
        for b in bid:
            bid_arr.append({
                'id': b.pk,
                'status': b.status,
                'description': b.description,
                'created_at': b.created_at,
            })
        
            products = BidProduct.objects.filter(bid__pk=b.pk)
            for p in products:
                b['products'].append({
                    'id': p.pk,
                    'name': p.product.name,
                    'amount': p.amount
                })
        
        
        return Response(status=200, data=bid_arr)