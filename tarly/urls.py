from django.contrib import admin
from django.urls import path

from shops.views import ShopView, SaleVew

urlpatterns = [
    path('admin/', admin.site.urls),
    path('publishers/<int:publisher_pk>/', ShopView.as_view()),
    path('sales/', SaleVew.as_view())
]
