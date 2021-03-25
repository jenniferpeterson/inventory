from django.contrib import admin

from .models import User, Category, Location, Item, StorageType, Household_request

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Item)
admin.site.register(StorageType)
admin.site.register(Household_request)
