import requests
from django.core.management.base import BaseCommand
from shop.models import SubCategory, Brand, Product


class Command(BaseCommand):
    help = 'Import products from an external API and save them to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting the product import process...'))
        save_products_from_api()


def save_products_from_api():
    api_url = 'http://128.65.179.44:2220/api/AllProduct?Idcode=QWElk25%$^][256WNmb>}<2200AH00sh'

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            for item in data:
                name = item.get('Name_product')
                barcode = item.get('Barcode')
                consumer_price = item.get('Consumer_price')
                sales_price = item.get('Sales_price')
                discount = item.get('Percent')
                inventory = item.get('Inventory')
                id_group = item.get('Id_group')

                try:
                    subcategory = SubCategory.objects.get(id=id_group)
                    # brand = Brand.objects.get(name=item.get('Brand_name'))  # Assuming you have a field for brand name

                    # Check for existing product by barcode
                    existing_product = Product.objects.filter(barcode=barcode).first()
                    if existing_product:
                        print(f"Skipping duplicate Barcode: {barcode}")
                    else:
                        product = Product(
                            name=name,
                            barcode=barcode,
                            price=sales_price,
                            discount_percentage=discount,
                            in_storage_count=inventory,
                            subcategory=subcategory,
                            # brand=brand,
                            description=item.get('Description', ''),
                        )
                        product.save()
                        print(f'Product {name} saved.')
                except SubCategory.DoesNotExist:
                    print(f"SubCategory with id {id_group} does not exist.")
                except Brand.DoesNotExist:
                    print(f"Brand does not exist for product {name}.")

            print("Products imported successfully.")
        else:
            print(f"Failed API request. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
