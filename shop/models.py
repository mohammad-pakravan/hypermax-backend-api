from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='subcategory_images/')
    parent = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brand_images/')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_images/')
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE,null=True,blank=True)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    barcode = models.CharField(max_length=100)
    is_promoted = models.BooleanField(default=False)
    in_storage_count = models.IntegerField()

    def __str__(self):
        return self.name


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Establish a one-to-one relationship

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_custom_user(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_custom_user(sender, instance, **kwargs):
    instance.customuser.save()
