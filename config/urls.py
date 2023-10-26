from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('warehouses/', include('warehouses.urls')),
    path('products/', include('products.urls')),
    path('objects/', include('objects.urls')),
    path('bid/', include('bid.urls')),
    path('drivers/', include('cars.urls')),
]

urlpatterns += swagger
