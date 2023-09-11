from django.urls import path
from .views import ObjectList, ObjectCreate, ObjectEdit, ObjectDelete, ObjectDetail


urlpatterns = [
    path('list', ObjectList.as_view()),
    path('create', ObjectCreate.as_view()),
    path('edit/<int:pk>', ObjectEdit.as_view()),
    path('delete/<int:pk>', ObjectDelete.as_view()),
    path('view/<int:pk>', ObjectDetail.as_view()),
]