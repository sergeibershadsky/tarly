from django.core.exceptions import ValidationError
from django.db import models

from books.models import Book


class BookShop(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class BookShopAbstract(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shop = models.ForeignKey(BookShop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        abstract = True


class Stock(BookShopAbstract):
    @classmethod
    def is_available(
            cls,
            book: int,
            shop: int,
            qty: int = 0
    ) -> bool:
        """ Check weather is book available in current store"""
        return cls.objects.filter(book_id=book, shop_id=shop, quantity__gt=qty).exists()

    class Meta:
        unique_together = ('book', 'shop')


class Sale(BookShopAbstract):
    date = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.stock_operations()
        super().save(force_insert, force_update, using, update_fields)

    def stock_operations(self):
        stock = Stock.objects.get(shop=self.shop, book=self.book)
        stock.quantity -= self.quantity
        stock.save()

    def clean(self):
        if not Stock.is_available(self.book.id, self.shop.id, self.quantity):
            raise ValidationError(f'Insufficient stock for {self.book}')
        return super(Sale, self).clean()
