from django.urls import path
from .views import ProductCreate


urlpatterns = [
    path('create', ProductCreate.as_view())
]