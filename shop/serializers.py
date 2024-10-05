from rest_framework import serializers
from .models import Category, SubCategory, Brand, Product


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'image', 'parent']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'subcategories']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'brand', 'subcategory', 'price', 'discount_percentage',
                  'description', 'barcode', 'is_promoted', 'in_storage_count']
