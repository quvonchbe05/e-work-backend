from django.urls import path
from .views import (
    ProductFirstCreate, 
    ProductList, 
    ProductSAdminEdit, 
    # ProductSearchForS, 
    Units, 
    ProductEditedList,
    ProductByWarehouseList
)


urlpatterns = [
    path('create', ProductFirstCreate.as_view()),
    path('list', ProductList.as_view()),
    path('list/edited', ProductEditedList.as_view()),
    path('sadmin/edit', ProductSAdminEdit.as_view()),
    path('list/warehouse/<int:pk>', ProductByWarehouseList.as_view()),
    path('units', Units.as_view()),
    # path('search/<str:product_name>', ProductSearchForS.as_view()),
]