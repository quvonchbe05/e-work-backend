from django.shortcuts import render
from rest_framework import generics
from .models import Driver
from .seralizers import DriverSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Create your views here.
