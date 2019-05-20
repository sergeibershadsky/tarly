from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from .models import BookShop, Sale, Stock


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def validate_quantity(self, qty):
        if not Stock.is_available(book=self.initial_data['book'],
                                  shop=self.initial_data['shop'],
                                  qty=qty):
            raise ValidationError(f'Insufficient stock for {qty}')
        return qty


class BookShopSerializer(serializers.ModelSerializer):
    books_sold_count = serializers.SerializerMethodField()
    books_in_stock = serializers.SerializerMethodField()

    def __init__(self, instance=None, data=empty, **kwargs):
        self.publisher = kwargs['context']['publisher']
        super().__init__(instance, data, **kwargs)

    def get_books_in_stock(self, store):
        return [
            {'id': stock.id, 'title': stock.book.title, 'copies_in_stock': stock.quantity}
            for stock in Stock.objects.filter(book__publisher=self.publisher, shop=store)
        ]

    def get_books_sold_count(self, store):
        return Sale.objects.filter(
            shop=store,
            book__publisher=self.publisher
        ).aggregate(
            Sum('quantity')
        )['quantity__sum']

    class Meta:
        model = BookShop
        fields = ('id', 'name', 'books_sold_count', 'books_in_stock')
