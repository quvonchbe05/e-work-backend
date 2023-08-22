from django.urls import path
from .views import ProductFirstCreate, ProductList, ProductSearchForS


urlpatterns = [
    path('create/first', ProductFirstCreate.as_view()),
    path('search/<str:product_name>', ProductSearchForS.as_view()),
    path('list', ProductList.as_view()),
]