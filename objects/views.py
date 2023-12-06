from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from bid.models import Bid, BidProduct, ObjectProductBase
from .models import Object
from .serializers import ObjectSerializer, ObjectListSerializer


# Create your views here.
class ObjectList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Object.objects.all()
    serializer_class = ObjectListSerializer


class ObjectCreate(generics.CreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer


class ObjectEdit(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer


class ObjectDelete(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer


class ObjectDetail(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        object = Object.objects.filter(pk=pk).first()
        if not object:
            return Response(status=404, data={'error': 'Obyekt topilmadi'})

        products = ObjectProductBase.objects.filter(object=object)

        obj_json = {
            'id': object.pk,
            'name': object.name,
            'address': object.address,
            'worker': {
                'id': object.worker.pk,
                'name': object.worker.name,
                'phone': object.worker.phone,
            },
            'bids': [],
            'products': [],
        }

        for p in products:
            obj_json['products'].append(
                {
                    "id": p.product.pk,
                    "name": p.product.name,
                    "price": p.product.price,
                    "total_price": p.total_price,
                    "amount": p.amount,
                    "created_at": p.created_at
                }
            )

        bid = Bid.objects.filter(object__pk=object.pk)
        bid_arr = []

        for b in bid:
            obj_json['bids'].append(
                {
                    "id": b.pk,
                    "status": b.status,
                    "description": b.description,
                    "created_at": b.created_at,
                    "total_summa": 0,
                    "products": [],
                }
            )

        for b in obj_json['bids']:
            products = BidProduct.objects.filter(bid__pk=b["id"])
            for p in products:
                b['total_summa'] = p.amount * int(p.product.price)
                b["products"].append(
                    {"id": p.pk, "name": p.product.name, "amount": p.amount, 'size': p.product.size}
                )

        return Response(status=200, data=obj_json)
