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
    bid = models.ManyToManyField(Listing, blank=True, related_name="current_bid")
    bidder = models.ManyToManyField(User, blank=True, related_name="name_bidder")
    list_name = models.ManyToManyField(Listing, blank=True, related_name="all_listings")
    
    def __str__(self) -> str:
        return f"{self.list_name}: {self.bid}"

class Comment(models.Model):
    username = models.CharField(max_length=64) #username
    comment = models.TextField

    def __str__(self) -> str:
        return f"{self.username}: {self.comment}"
