"""
Seed the database with demo data so a freshly deployed ShopeSphere instance
isn't empty.

Usage:
    python manage.py seed_data              # add sample data (safe to re-run)
    python manage.py seed_data --flush       # wipe seeded data first, then re-add

Idempotent: products are matched on name, so running this more than once
won't create duplicates. Nothing here touches real user-entered data
(carts, orders, addresses) — it only creates/updates catalog `Product`s,
a `Delivery` pricing row, and one demo login.
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from base.models import Delivery, Product

SAMPLE_PRODUCTS = [
    # (category, name, desc, price, sale, trending)
    ("Electronics", "Wireless Mouse", "Ergonomic 2.4GHz wireless mouse with silent clicks.", "499.00", False, True),
    ("Electronics", "Mechanical Keyboard", "Compact 87-key mechanical keyboard, blue switches.", "2499.00", True, True),
    ("Electronics", "Bluetooth Headphones", "Over-ear headphones with 30-hour battery life.", "1899.00", True, False),
    ("Electronics", "Smartwatch", "Fitness smartwatch with heart-rate and SpO2 tracking.", "3299.00", False, True),
    ("Fashion", "Men's Casual Shirt", "Cotton slim-fit casual shirt, machine washable.", "899.00", False, False),
    ("Fashion", "Women's Running Shoes", "Lightweight breathable running shoes.", "1799.00", True, True),
    ("Fashion", "Denim Jacket", "Classic unisex denim jacket.", "1599.00", False, False),
    ("Home", "Ceramic Coffee Mug Set", "Set of 4 ceramic mugs, 300ml each.", "699.00", False, False),
    ("Home", "LED Desk Lamp", "Adjustable brightness LED desk lamp with USB port.", "999.00", True, False),
    ("Books", "Django for Beginners", "A hands-on introduction to building web apps with Django.", "1299.00", False, True),
    ("Books", "Clean Code", "A handbook of agile software craftsmanship.", "1099.00", False, False),
    ("Beauty", "Herbal Face Wash", "Gentle daily face wash with neem and tulsi extracts.", "349.00", True, False),
]

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo1234"


class Command(BaseCommand):
    help = "Populate the database with demo products, delivery pricing, and a demo login."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete previously seeded products/delivery rows before re-creating them.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            names = [p[1] for p in SAMPLE_PRODUCTS]
            deleted, _ = Product.objects.filter(name__in=names).delete()
            Delivery.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Flushed {deleted} seeded product(s) and all Delivery rows."))

        created_count = 0
        updated_count = 0
        for category, name, desc, price, sale, trending in SAMPLE_PRODUCTS:
            obj, created = Product.objects.update_or_create(
                name=name,
                defaults={
                    "category": category,
                    "desc": desc,
                    "price": Decimal(price),
                    "sale": sale,
                    "trending": trending,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
        self.stdout.write(
            self.style.SUCCESS(f"Products: {created_count} created, {updated_count} updated.")
        )

        # A single Delivery row holds the app's payment/shipping pricing
        # (see Payment_method view in base/views.py, which reads
        # Delivery.objects.first()). Model field defaults are sensible, so
        # just make sure exactly one row exists.
        if not Delivery.objects.exists():
            Delivery.objects.create()
            self.stdout.write(self.style.SUCCESS("Created default Delivery pricing row."))
        else:
            self.stdout.write("Delivery pricing row already exists, left untouched.")

        # Demo login so you can click through cart/checkout right after deploying.
        # NOTE: authent/views.py currently compares plaintext passwords (see
        # README "Security notes"), so this intentionally stores the password
        # in plaintext too, to match the app's existing (insecure) login
        # logic rather than create an account that can't actually log in.
        user, created = User.objects.get_or_create(
            username=DEMO_USERNAME,
            defaults={"email": "demo@example.com", "password": DEMO_PASSWORD},
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created demo login -> username: {DEMO_USERNAME} / password: {DEMO_PASSWORD}")
            )
        else:
            self.stdout.write(f"Demo user '{DEMO_USERNAME}' already exists, left untouched.")

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
