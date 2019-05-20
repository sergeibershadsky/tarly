from django.contrib import admin
from .models import BookShop, Stock, Sale


class StockInline(admin.StackedInline):
    model = Stock
    extra = 0


@admin.register(BookShop)
class BookShopAdmin(admin.ModelAdmin):
    inlines = [StockInline, ]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('book', 'shop', 'quantity', 'date',)
