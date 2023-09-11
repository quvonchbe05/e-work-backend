from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, UserCreateSerializer, UserFirstEditSerializer, UserListSerializer, UserEditSerilizer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
import random
from .utils import decode_jwt

# Create your views here.





class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                token = RefreshToken.for_user(user)
                return Response(status=200, data={
                    'token': str(token.access_token),
                    'username': user.username,
                    'role': user.role,
                    'status': user.status,
                })
            else:
                return Response(status=401, data={'error': 'Invalid username or password'})
        else:
            return Response(status=400, data={'error': serializer.errors})
    
 
 
 
    
    
    
class UserFirtEdit(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=UserFirstEditSerializer)
    def post(self, request):
        serializer = UserFirstEditSerializer(data=request.data)
        if serializer.is_valid():
            user = decode_jwt(request)
            updated_user = get_object_or_404(CustomUser, id=user['user_id'])
            updated_user.name=request.data['name']
            updated_user.phone=request.data['phone']
            if len(request.data['username']) and request.data['username'] != updated_user.username:
                updated_user.username=request.data['username']
            if len(request.data['password']):
                updated_user.password=make_password(request.data['password'])
            updated_user.status=True
            # updated_user.is_superuser=True
            updated_user.save()
            return Response(
                status=201,
                data={
                    'name':updated_user.name,
                    'phone':updated_user.phone,
                    'username':updated_user.username,
                    'role':updated_user.role,
                    'status':updated_user.status,
                }
            )
        else:
            return Response(status=400, data={'error': serializer.errors})
        
        





class UserCreate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request):
        random_password = get_random_string(length=8)
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_user = CustomUser(
                name=request.data['name'],
                phone=request.data['phone'],
                username = request.data['username'],
                role = request.data['role'],
                password = make_password(random_password),
            )
            new_user.save()
            return Response(
                status=201,
                data={
                    'name':new_user.name,
                    'phone':new_user.phone,
                    'username':new_user.username,
                    'role':new_user.role,
                    'status':new_user.status,
                }
            )
        else:
            return Response(status=400, data={'error': serializer.errors})
        
        
        
        
        
        
        
class GenerateNewPassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        new_passwrod = str(random.randint(11111111, 99999999))
        user = get_object_or_404(CustomUser, id=pk)
        if user is not None:
            user.password = make_password(new_passwrod)
            user.save()
            return Response(status=201, data={'password': new_passwrod}) 
        else:
            return Response(status=404, data={'error': "User not found!"})







class UserList(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(role='s_admin').order_by('-pk')
    serializer_class = UserListSerializer
 






class UserEdit(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(role='s_admin').order_by('-pk')
    serializer_class = UserEditSerilizer
    
    
    
    
    
    
    
class UserDelete(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(role='s_admin').order_by('-pk')
    serializer_class = UserEditSerilizer
    
    
    
    
    
    
    
class UserDetail(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(role='s_admin').order_by('-pk')
    serializer_class = UserListSerializer
    
    
    
    
    
    
    
class UserMe(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        token = decode_jwt(request)
        user = get_object_or_404(CustomUser, id=token['user_id'])
        serializer = UserListSerializer(user)
        return Response(
            status=200,
            data=serializer.data
        )