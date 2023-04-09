from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class UserBid(admin.TabularInline):
    model = Bid

class UserComment(admin.TabularInline):
    model = Comment

class UserListing(admin.TabularInline):
    model = ActiveListing

class CustomUserAdmin(UserAdmin):
    inlines = [UserListing, UserBid, UserComment ]
    list_display = ["username", "email"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("user_listings", "user_bids", "user_comments")
        return queryset

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(ActiveListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist)