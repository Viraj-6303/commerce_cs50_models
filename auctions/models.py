from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class ActiveListing(models.Model):
    listing_title = models.CharField(max_length=64, blank=False)
    price = models.IntegerField(blank=False)
    description = models.CharField(max_length=128, blank=False)
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    category = models.CharField(max_length=16)
    image = models.URLField()

    def __str__(self):
        return f'{self.listing_title}, Listed By: {self.listing_user}'

class Bid(models.Model):
    title = models.ForeignKey(ActiveListing, on_delete=models.CASCADE, related_name="total_bids")
    bids = models.DecimalField(max_digits=8, decimal_places=2)
    bidding_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")

    def __str__(self):
        return f'Title: {self.title.listing_title}, Bidding Price: {self.bids}, Listed By: {self.bidding_user}'

class Comment(models.Model):
    title = models.ForeignKey(ActiveListing, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=512)
    commented_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")

    def __str__(self):
        return f'Title: {self.title.listing_title}, User: {self.commented_user}'