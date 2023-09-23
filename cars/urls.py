from django.urls import path
from .views import DriverList, DriverCreate, DriverEdit, DriverDelete, DriverDetail


urlpatterns = [
    path('list', DriverList.as_view()),
    path('create', DriverCreate.as_view()),
    path('edit/<int:pk>', DriverEdit.as_view()),
    path('delete/<int:pk>', DriverDelete.as_view()),
    path('view/<int:pk>', DriverDetail.as_view()),
]