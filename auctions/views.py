from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *



def index(request):
    if request.method == "POST":
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        listing_category = request.POST["category"]
        listing_category_obj = Category.objects.get(cat_name = listing_category)
        image = request.POST["url"]
        user = User.objects.get(username=request.user.username)
        try:
            ActiveListing(active = 1,  listing_title = title, price = price, description = description, listing_user = user, category = listing_category_obj, image = image).save()
        except IntegrityError:
            messages.error(request, "A similar entry already exists")
            return render(request, "auctions/create.html")
        return render(request, "auctions/index.html", {
            "listings" : ActiveListing.objects.all(),
            "page" : "index",
        })
    return render(request, "auctions/index.html", {
        "listings" : ActiveListing.objects.all(),
        "page" : "index",
    })

def create_listing(request):
    return render(request, "auctions/create.html",{
        "categories" : Category.objects.all(),
    })

def listing(request, name):
    if Watchlist.objects.filter(user=request.user, listings=ActiveListing.objects.get(listing_title=name)).exists():
        watchlist = True
    else:
        watchlist = False
    user = User.objects.get(username=request.user.username)
    title = ActiveListing.objects.get(listing_title=name)
    max
    start_price = title.price
    max_bid_user = 0
    if Bid.objects.filter(title=ActiveListing.objects.get(listing_title=name)).exists():
        max_bid = Bid.objects.filter(title=ActiveListing.objects.get(listing_title=name)).aggregate(Max('bids'))['bids__max']
        max_bid_user = Bid.objects.get(bids=max_bid).bidding_user
    else:
        max_bid = start_price
    
    
    if request.method == "POST":

        if "watchlist" in request.POST:
            Watchlist(user=request.user, listings=title).save()
            return HttpResponseRedirect(reverse("listing", kwargs={'name':name}))
            
        if "watchlisted" in request.POST:
            Watchlist.objects.filter(user=request.user, listings=title).delete()
            return HttpResponseRedirect(reverse("listing", kwargs={'name':name}))

        if "close" in request.POST:
            title.active = 0
            title.save()
            return HttpResponseRedirect(reverse("listing", kwargs={'name':name}))
        
        if "comments" in request.POST:
            comments = request.POST["comments"]
            Comment(title = title, comment = comments, commented_user = user).save()
            return render(request, "auctions/listing.html",{
                "title" : ActiveListing.objects.get(listing_title=name),
                "comments" : ActiveListing.objects.get(listing_title=name).comments.all(),
                "user": user,
                "max_bid" : max_bid,
                "watchlist" : watchlist,    
            })
        
        if "bid" in request.POST:
            bids = request.POST["bid"]
            if float(bids) <= title.price or float(bids) <= max_bid :
                messages.error(request, "The bid is lower than the starting price or highest bid")
            else:
                Bid(bidding_user = request.user, bids = bids, title = title).save()
                max_bid = Bid.objects.filter(title=ActiveListing.objects.get(listing_title=name)).aggregate(Max('bids'))['bids__max']
                max_bid_user = Bid.objects.get(bids=max_bid).bidding_user
                return render(request, "auctions/listing.html",{
                    "title" : ActiveListing.objects.get(listing_title=name),
                    "bids" : ActiveListing.objects.get(listing_title=name).total_bids.all(),
                    "user": user,
                    "max_bid" : max_bid,
                    "watchlist" : watchlist,
                    "bid_num" : ActiveListing.objects.get(listing_title=name).total_bids.count(), 
                    "max_bid_user" : max_bid_user,  
                })
    if max_bid_user:
        return render(request, "auctions/listing.html",{
            "title" : ActiveListing.objects.get(listing_title=name),
            "comments" : ActiveListing.objects.get(listing_title=name).comments.all(),
            "user": user,
            "max_bid" : max_bid,
            "max_bid_user" : max_bid_user,
            "watchlist" : watchlist,
            "bid_num" : ActiveListing.objects.get(listing_title=name).total_bids.count(),
        })
    else:
        return render(request, "auctions/listing.html",{
            "title" : ActiveListing.objects.get(listing_title=name),
            "comments" : ActiveListing.objects.get(listing_title=name).comments.all(),
            "user": user,
            "max_bid" : max_bid,
            "max_bid_user" : 0,
            "watchlist" : watchlist,
            "bid_num" : ActiveListing.objects.get(listing_title=name).total_bids.count(),
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def category(request):
    return render(request, "auctions/category.html",{
        "categories" : Category.objects.all(),
    })

def c_listings(request, id):
    return render(request, "auctions/index.html",{
        "listings" : ActiveListing.objects.filter(category=id),
        "page" : "category",
        "cat" : Category.objects.get(id=id).cat_name, 
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "listings" : Watchlist.objects.filter(user=request.user),
        "page" : "watchlist",
    })