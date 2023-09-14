from django.urls import path
from .views import (
    CreateBidForM,
    BidMyList,
    GetBidById,
    BidList,
)

urlpatterns = [
    path('object/create', CreateBidForM.as_view()),
    path('object/history', BidMyList.as_view()),
    path('view/<int:pk>', GetBidById.as_view()),
    path('list', BidList.as_view()),
]