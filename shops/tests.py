import random

from django.apps import apps
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework import status

from books.models import Publisher, Book
from .apps import ShopsConfig
from .models import BookShop, Stock


class ShopsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.publisher1 = mommy.make(Publisher)
        cls.publisher2 = mommy.make(Publisher)
        cls.shop1 = mommy.make(BookShop)
        cls.shop2 = mommy.make(BookShop)
        cls.book1 = mommy.make(Book)
        cls.book2 = mommy.make(Book)
        mommy.make(Stock, book=cls.book1, shop=cls.shop1, quantity=random.randint(20, 100))
        mommy.make(Stock, book=cls.book1, shop=cls.shop2, quantity=random.randint(20, 100))
        mommy.make(Stock, book=cls.book2, shop=cls.shop2, quantity=random.randint(20, 100))

    def test_apps(self):
        self.assertEqual(ShopsConfig.name, 'shops')
        self.assertEqual(apps.get_app_config('shops').name, 'shops')

    def test_sales(self):
        old_quantity = Stock.objects.get(book=self.book1, shop=self.shop1).quantity
        sale = random.randint(1, Stock.objects.get(book=self.book1, shop=self.shop1).quantity)
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
        self.assertEqual(el['shop'], self.shop1.id)
        self.assertEqual(el['book'], self.book1.id)
        self.assertEqual(el['quantity'], sale)

        self.assertEqual(
            first=old_quantity - sale,
            second=Stock.objects.get(book=self.book1, shop=self.shop1).quantity
        )
