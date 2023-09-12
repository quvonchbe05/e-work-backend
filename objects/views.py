from django.shortcuts import render
from rest_framework import generics
from .models import Object
from .serializers import ObjectSerializer, ObjectListSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

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
    
    
    
    
    
class ObjectDetail(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Object.objects.all()
    serializer_class = ObjectListSerializer