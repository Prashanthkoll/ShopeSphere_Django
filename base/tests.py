from decimal import Decimal
from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from base.models import AddCard, Delivery, Product


class ProductModelTests(TestCase):
    def test_product_str_and_defaults(self):
        product = Product.objects.create(
            category="Electronics",
            name="Wireless Mouse",
            desc="A basic wireless mouse",
            price=Decimal("499.00"),
        )
        self.assertEqual(product.name, "Wireless Mouse")
        self.assertFalse(product.sale)
        self.assertFalse(product.trending)


class HomePageTests(TestCase):
    def setUp(self):
        Product.objects.create(
            category="Electronics",
            name="Wireless Mouse",
            desc="A basic wireless mouse",
            price=Decimal("499.00"),
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Mouse")

    def test_home_page_search_filters_products(self):
        Product.objects.create(
            category="Books",
            name="Django for Beginners",
            desc="A book about Django",
            price=Decimal("999.00"),
        )
        response = self.client.get(reverse("home"), {"query": "Django"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django for Beginners")
        self.assertNotContains(response, "Wireless Mouse")


class CartViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="shopper", password="testpass123")
        self.product = Product.objects.create(
            category="Electronics",
            name="Keyboard",
            desc="A mechanical keyboard",
            price=Decimal("2500.00"),
        )

    def test_cart_requires_login(self):
        response = self.client.get(reverse("cart"))
        self.assertNotEqual(response.status_code, 200)

    def test_add_to_cart_creates_addcard_entry(self):
        self.client.login(username="shopper", password="testpass123")
        response = self.client.get(reverse("addcart", args=[self.product.id]))
        self.assertIn(response.status_code, (200, 302))
        self.assertTrue(
            AddCard.objects.filter(host=self.user, name=self.product.name).exists()
        )

    def test_cart_page_loads_when_logged_in(self):
        self.client.login(username="shopper", password="testpass123")
        response = self.client.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)


class SeedDataCommandTests(TestCase):
    def test_seed_data_creates_products_and_delivery_row(self):
        out = StringIO()
        call_command("seed_data", stdout=out)

        self.assertGreater(Product.objects.count(), 0)
        self.assertEqual(Delivery.objects.count(), 1)
        self.assertTrue(User.objects.filter(username="demo").exists())

    def test_seed_data_is_idempotent(self):
        call_command("seed_data", stdout=StringIO())
        first_count = Product.objects.count()

        call_command("seed_data", stdout=StringIO())
        second_count = Product.objects.count()

        self.assertEqual(first_count, second_count)
        self.assertEqual(Delivery.objects.count(), 1)