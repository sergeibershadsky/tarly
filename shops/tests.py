import random

from django.apps import apps
from django.db.models import Sum
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from books.models import Publisher, Book
from .apps import ShopsConfig
from .models import BookShop, Stock, Sale


class ShopsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.publisher1 = mommy.make(Publisher)
        cls.publisher2 = mommy.make(Publisher)
        cls.shop1 = mommy.make(BookShop)
        cls.shop2 = mommy.make(BookShop)
        cls.book1 = mommy.make(Book, publisher=cls.publisher1)
        cls.book2 = mommy.make(Book, publisher=cls.publisher2)
        mommy.make(Stock, book=cls.book1, shop=cls.shop1, quantity=random.randint(20, 100))
        mommy.make(Stock, book=cls.book1, shop=cls.shop2, quantity=random.randint(20, 100))
        mommy.make(Stock, book=cls.book2, shop=cls.shop2, quantity=random.randint(20, 100))

    def test_apps(self):
        self.assertEqual(ShopsConfig.name, 'shops')
        self.assertEqual(apps.get_app_config('shops').name, 'shops')

    def test_sales(self):
        old_quantity = Stock.available_count(book=self.book1, shop=self.shop1)
        sale = random.randint(1, Stock.available_count(book=self.book1, shop=self.shop1))
        response = self.client.post(reverse('sales'), data={
            'shop': self.shop1.id,
            'book': self.book1.id,
            'quantity': sale
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse('sales'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 1)
        el = response.json()[0]
        self.assertEqual(el.get('shop'), self.shop1.id)
        self.assertEqual(el.get('book'), self.book1.id)
        self.assertEqual(el.get('quantity'), sale)

        self.assertEqual(
            first=old_quantity - sale,
            second=Stock.objects.get(book=self.book1, shop=self.shop1).quantity
        )

    def test_publisher_api(self):
        mommy.make(Sale,
                   book=self.book1,
                   shop=self.shop1,
                   quantity=random.randint(1, Stock.available_count(self.book1, self.shop1))
                   )
        mommy.make(Sale,
                   book=self.book1,
                   shop=self.shop2,
                   quantity=random.randint(1, Stock.available_count(self.book1, self.shop2))
                   )
        response = self.client.get(reverse('publisher', kwargs={'publisher_pk': self.publisher1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn('shops', body)
        shops = body['shops']
        self.assertEqual(len(shops), 2)

        for shop in shops:
            self.assertListEqual(['id', 'name', 'books_sold_count', 'books_in_stock'], list(shop))
            shop_model = BookShop.objects.get(pk=shop['id'])
            self.assertEqual(shop_model.id, shop['id'])
            self.assertEqual(shop_model.name, shop['name'])
            self.assertEqual(
                shop['books_sold_count'],
                shop_model.sale_set.filter(book__publisher=self.publisher1).aggregate(Sum('quantity'))['quantity__sum'])
            self.assertEqual(len(shop['books_in_stock']), 1)
            book_in_stock = shop['books_in_stock'][0]
            self.assertEqual(['id', 'title', 'copies_in_stock'], list(book_in_stock))

        books_sold_count = [shop['books_sold_count'] for shop in shops]
        self.assertListEqual(books_sold_count, sorted(books_sold_count))
