from django.urls import path
from .views import (
    CreateBidForM,
    BidMyList,
    GetBidById,
    BidList,
    ComparisonBidById,
    CreateBidToWarehouse,
)

urlpatterns = [
    path('object/create', CreateBidForM.as_view()),
    path('object/history', BidMyList.as_view()),
    path('view/<int:pk>', GetBidById.as_view()),
    path('list', BidList.as_view()),
    path('comparison/<int:pk>', ComparisonBidById.as_view()),
    path('warehouse/to/<int:pk>', CreateBidToWarehouse.as_view()),
]