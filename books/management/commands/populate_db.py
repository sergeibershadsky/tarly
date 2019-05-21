from django.core.management.base import BaseCommand
from mimesis import Text, Business

from books.models import Book, Publisher
from shops.models import BookShop, Stock, Sale
import random


class Command(BaseCommand):
    help = 'Populate database with data'

    def handle(self, *args, **options):

        for _ in range(10):
            _publisher = Business()
            publisher = Publisher.objects.create(name=_publisher.company())

            for _book in range(50):
                _text = Text()
                Book.objects.create(title=_text.title(), publisher=publisher, annotation=_text.text(10))

            for s in range(6):
                _shop = Business()
                shop = BookShop.objects.create(name=_shop.company())

                for stock_book in random.sample(list(Book.objects.all()), 25):
                    Stock.objects.create(
                        book=stock_book,
                        shop=shop,
                        quantity=random.randint(10, 50)
                    )

                for stock_sale in random.sample(list(shop.stock_set.all()), 20):
                    Sale.objects.create(
                        book=stock_sale.book,
                        shop=stock_sale.shop,
                        quantity=random.randint(2, stock_sale.quantity)
                    )
