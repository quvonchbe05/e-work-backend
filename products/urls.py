from django.urls import path
from .views import ProductFirstCreate, ProductList, ProductSearchForS, ProductSAdminEdit, Units, ProductTrueList, ProductFalseList, ProductEditedList


urlpatterns = [
    path('create/first', ProductFirstCreate.as_view()),
    path('search/<str:product_name>', ProductSearchForS.as_view()),
    path('sadmin/edit', ProductSAdminEdit.as_view()),
    path('list', ProductList.as_view()),
    path('units', Units.as_view()),
    path('list/incoming', ProductTrueList.as_view()),
    path('list/outgoing', ProductFalseList.as_view()),
    path('list/edited', ProductEditedList.as_view()),
]