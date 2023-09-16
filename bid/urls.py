from django.urls import path
from .views import (
    CreateBidForM,
    BidMyList,
    GetBidById,
    BidList,
    ComparisonBidById,
    CreateBidToWarehouse,
    CancelBid,
    ConfirmInWarehouse,
)

urlpatterns = [
    path('object/create', CreateBidForM.as_view()),
    path('object/history', BidMyList.as_view()),
    path('view/<int:pk>', GetBidById.as_view()),
    path('list', BidList.as_view()),
    path('comparison/<int:pk>', ComparisonBidById.as_view()),
    path('warehouse/to/', CreateBidToWarehouse.as_view()),
    path('cancel/<int:pk>', CancelBid.as_view()),
    path('warehouse/confirm/<int:pk>', ConfirmInWarehouse.as_view()),
]