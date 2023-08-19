from django.urls import path
from .views import WarehouseList, WarehouseCreate, WarehouseEdit, WarehouseDelete, WarehouseDetail


urlpatterns = [
    path('list', WarehouseList.as_view()),
    path('create', WarehouseCreate.as_view()),
    path('edit/<int:pk>', WarehouseEdit.as_view()),
    path('delete/<int:pk>', WarehouseDelete.as_view()),
    path('view/<int:pk>', WarehouseDetail.as_view()),
]