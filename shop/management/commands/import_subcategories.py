import requests
from django.core.management.base import BaseCommand
from shop.models import SubCategory, Category

class Command(BaseCommand):
    help = 'Import subcategories from an external API and save them to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting the subcategory import process...'))
        save_subcategories_from_api()

def save_subcategories_from_api():
    api_url = 'http://128.65.179.44:2220/api/ListGroup?Idcode=QWElk25%$^][256WNmb>}<2200AH00sh'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        for item in data:
            cat_Id = item['Id']
            Name_group = item['Name_group']
            Id_parent = item['Id_parent']
            Has_child = item['Has_child']

            if Id_parent == 0:
                # Create a new Category instance
                existing_category = Category.objects.filter(id=cat_Id).first()
                if not existing_category:
                    category = Category(
                        id=cat_Id,
                        name=Name_group,
                        # Add image handling if available
                    )
                    category.save()
                    print(f'Category {Name_group} saved.')
            else:
                # Create a new SubCategory instance
                existing_subcategory = SubCategory.objects.filter(id=cat_Id).first()
                if not existing_subcategory:
                    try:
                        parent_category = Category.objects.get(id=Id_parent)
                    except Category.DoesNotExist:
                        # Create a new parent category if it doesn't exist
                        parent_category = Category(
                            id=Id_parent,
                            name=f'New Category {Id_parent}',  # Placeholder name
                            # Add image handling if available
                        )
                        parent_category.save()
                        print(f'Parent Category {parent_category.name} created with ID {Id_parent}.')

                    # Now create the subcategory with the parent category
                    subcategory = SubCategory(
                        name=Name_group,
                        id=cat_Id,
                        parent=parent_category,
                        # Add image handling if available
                    )
                    subcategory.save()
                    print(f'SubCategory {Name_group} saved.')

        print("Subcategories imported successfully.")
    else:
        print(f"Failed API request. Status code: {response.status_code}")
