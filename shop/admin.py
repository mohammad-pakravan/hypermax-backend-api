from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'address')


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Product)
