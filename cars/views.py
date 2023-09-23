from django.shortcuts import render
from rest_framework import generics
from .models import Driver
from .seralizers import DriverSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Create your views here.
class DriverList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    
    
    
    
    
class DriverCreate(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    
    
    
    
    
class DriverEdit(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    
    
    
    
    
class DriverDelete(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    
    
    
    
    
class DriverDetail(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer