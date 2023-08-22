from django.urls import path
from .views import ProductFirstCreate, ProductList


urlpatterns = [
    path('create/first', ProductFirstCreate.as_view()),
    path('list', ProductList.as_view()),
]