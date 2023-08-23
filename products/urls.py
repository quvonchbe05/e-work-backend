from django.urls import path
from .views import (
    ProductFirstCreate, 
    ProductList, 
    ProductSAdminEdit, 
    # ProductSearchForS, 
    Units, 
    ProductEditedList,
    ProductByWarehouseList,
    ProductOutgoing,
    ProductOutgoingList,
    ProductWarehouseHistoryList,
    ProductWarehouseAllList,
)


urlpatterns = [
    path('create', ProductFirstCreate.as_view()),
    path('list', ProductList.as_view()),
    path('list/edited', ProductEditedList.as_view()),
    path('sadmin/edit', ProductSAdminEdit.as_view()),
    path('sadmin/outgoing', ProductOutgoing.as_view()),
    path('sadmin/list', ProductOutgoingList.as_view()),
    path('sadmin/history', ProductWarehouseHistoryList.as_view()),
    path('list/warehouse/<int:pk>', ProductByWarehouseList.as_view()),
    path('list/warehouse/all/<int:pk>', ProductWarehouseAllList.as_view()),
    path('units', Units.as_view()),
    # path('search/<str:product_name>', ProductSearchForS.as_view()),
]