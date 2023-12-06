from django.urls import path
from .views import LoginView, UserFirtEdit, UserCreate, GenerateNewPassword, UserList, UserEdit, UserDelete, UserDetail, \
    UserMe, LogoutView

urlpatterns = [
    path('auth/login', LoginView.as_view()),
    path('auth/users/first/edit', UserFirtEdit.as_view()),
    path('auth/users/me', UserMe.as_view()),
    path('auth/user/create', UserCreate.as_view()),
    path('auth/user/reset/password', GenerateNewPassword.as_view()),
    path('api/logout/', LogoutView.as_view()),

    path('workers/create', UserCreate.as_view()),
    path('workers/generate-password/<int:pk>', GenerateNewPassword.as_view()),
    path('workers/list', UserList.as_view()),
    path('workers/edit/<int:pk>', UserEdit.as_view()),
    path('workers/delete/<int:pk>', UserDelete.as_view()),
    path('workers/view/<int:pk>', UserDetail.as_view()),
]
