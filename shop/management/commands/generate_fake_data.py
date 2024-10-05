import random
from django.core.management.base import BaseCommand
from faker import Faker
from shop.models import Category, SubCategory, Brand, Product

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data for testing the API'

    def handle(self, *args, **kwargs):
        self.generate_categories_and_subcategories()
        self.generate_brands()
        self.generate_products()

    def generate_categories_and_subcategories(self):
        # Generate fake categories and subcategories
        for _ in range(5):
            category = Category.objects.create(
                name=fake.word(),
                image=fake.image_url()
            )
            print(f'Created Category: {category.name}')

            # Create subcategories for each category
            for _ in range(random.randint(1, 4)):
                subcategory = SubCategory.objects.create(
                    name=fake.word(),
                    image=fake.image_url(),
                    parent=category
                )
                print(f'  Created SubCategory: {subcategory.name}')

    def generate_brands(self):
        # Generate fake brands
        for _ in range(10):
            brand = Brand.objects.create(
                name=fake.company(),
                image=fake.image_url()
            )
            print(f'Created Brand: {brand.name}')

    def generate_products(self):
        # Get existing subcategories and brands
        subcategories = SubCategory.objects.all()
        brands = Brand.objects.all()

        if not subcategories or not brands:
            print('No subcategories or brands found, please run "generate_categories_and_subcategories" first.')
            return

        # Generate fake products
        for _ in range(20):
            product = Product.objects.create(
                name=fake.word(),
                image=fake.image_url(),
                brand=random.choice(brands),
                subcategory=random.choice(subcategories),
                price=random.uniform(10.0, 1000.0),
                discount_percentage=random.randint(0, 30),
                description=fake.text(),
                barcode=fake.ean(length=13),
                is_promoted=random.choice([True, False]),
                in_storage_count=random.randint(1, 100)
            )
            print(f'Created Product: {product.name}')
