from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

# Create your models here.


class User(AbstractUser):
    household = models.ManyToManyField("User", blank=True)

    def __str__(self):
        return f"{self.username}"


class Household_request(models.Model):
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return f"To: {self.to_user}, From: {self.from_user}"


class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category_name}"


class Location(models.Model):
    location = models.CharField(max_length=64)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by_loc")

    def __str__(self):
        return f"{self.location}"


class StorageType(models.Model):
    storage_type = models.CharField(max_length=64)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=True,  related_name="storage_location")
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by_stor")

    def __str__(self):
        return f"{self.storage_type} in {self.location} - Storage Owner: {self.created_by}"


class Item(models.Model):
    item_name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User, related_name="owner", on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=now)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,  related_name="item_category")
    img = models.URLField(blank=True)
    stored_in = models.ForeignKey(
        StorageType, on_delete=models.CASCADE, blank=True,  related_name="stored_in")

    def __str__(self):
        return f"{self.item_name} in {self.stored_in}"
