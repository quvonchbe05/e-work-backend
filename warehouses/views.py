from django.shortcuts import render
from rest_framework import generics
from .models import Warehouse
from .serializers import WarehouseSerializer, WarehouseListSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Create your views here.
class WarehouseList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseListSerializer
    
    
    
    
    
class WarehouseCreate(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    
    
    
    
    
class WarehouseEdit(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    
    
    
    
    
class WarehouseDelete(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    
    
    
    
    
class WarehouseDetail(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseListSerializer