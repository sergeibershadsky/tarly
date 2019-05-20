from django.apps import apps
from django.test import TestCase
from model_mommy import mommy

from books.models import Publisher
from .apps import ShopsConfig
from .models import BookShop


class ShopsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.publisher1 = mommy.make(Publisher)
        cls.publisher2 = mommy.make(Publisher)
        cls.shop1 = mommy.make(BookShop)
        cls.shop2 = mommy.make(BookShop)

    def test_apps(self):
        self.assertEqual(ShopsConfig.name, 'shops')
        self.assertEqual(apps.get_app_config('shops').name, 'shops')
