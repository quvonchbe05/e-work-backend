from django.urls import path,include
from .views import (
    CreateBitForM,
)

urlpatterns = [
    path('m/create', CreateBitForM.as_view()),
]