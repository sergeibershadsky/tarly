from django.contrib import admin
from django.urls import path
from rest_framework.documentation import include_docs_urls

from shops.views import ShopView, SaleVew

urlpatterns = [
    path('admin/', admin.site.urls),
    path('publishers/<int:publisher_pk>/', ShopView.as_view(), name='publisher'),
    path('sales/', SaleVew.as_view(), name='sales'),
    path('', include_docs_urls(title='Tarly API'))
]
