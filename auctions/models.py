from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    cat_name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.cat_name}'

class ActiveListing(models.Model):
    listing_title = models.CharField(max_length=64, blank=False, unique=True)
    price = models.IntegerField(blank=False)
    description = models.CharField(max_length=128, blank=False, unique=True)
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="cat_listings")
    image = models.URLField(unique=True)
    active = models.BooleanField()

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
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wl_listings")
    listings = models.ForeignKey(ActiveListing, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} watchlisted {self.listings}'
    
    class Meta:
        unique_together = ('user', 'listings')
