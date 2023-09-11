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
    ProductTemplateEdit,
    ProductTemplateDetail,
    PRoductTemplateDelete,
    Monitoring,
    WarehousesMonitoring,
    MonitoringChart,
    MonitoringLineChart,
    ProductTemplateHistory,
)


urlpatterns = [
    path('create', ProductFirstCreate.as_view()),
    path('edit/<int:pk>', ProductTemplateEdit.as_view()),
    path('detail/<int:pk>', ProductTemplateDetail.as_view()),
    path('delete/<int:pk>', PRoductTemplateDelete.as_view()),
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
    path('monitoring', Monitoring.as_view()),
    path('monitoring/warehouses', WarehousesMonitoring.as_view()),
    path('monitoring/chart', MonitoringChart.as_view()),
    path('monitoring/linechart', MonitoringLineChart.as_view()),
    
    path('list/view/<int:pk>', ProductTemplateHistory.as_view())
]