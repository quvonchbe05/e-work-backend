from django.urls import path,include
from .views import (
    CreateBidForM,
    BidMyList,
)

urlpatterns = [
    path('object/create', CreateBidForM.as_view()),
    path('object/history', BidMyList.as_view())
]