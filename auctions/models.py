from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.id}.{self.title}, {self.description}: {self.price}"

class Bidding(models.Model):
    list_name = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="all_listings")
    bid = models.PositiveIntegerField

    def __str__(self) -> str:
        return f"{self.list_name}: {self.bid}"

class Comments(models.Model):
    username = models.CharField(max_length=64) #username
    comment = models.TextField

    def __str__(self) -> str:
        return f"{self.username}: {self.comment}"
