from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

category = []

def index(request):
    if request.method == "POST":
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        listing_category = request.POST["category"]
        image = request.POST["url"]
        user = User.objects.get(username=request.user.username)
        ActiveListing(listing_title = title, price = price, description = description, listing_user = user, category = listing_category, image = image).save()
        if listing_category.lower() not in category:
            category.append(listing_category)
        return render(request, "auctions/index.html", {
            "listings" : ActiveListing.objects.all()
        })
    return render(request, "auctions/index.html", {
        "listings" : ActiveListing.objects.all()
    })

def create_listing(request):
    return render(request, "auctions/create.html")

def listing(request, name):
    if request.method == "POST":
        comments = request.POST["comments"]
        username = User.objects.get(username=request.user.username)
        title = ActiveListing.objects.get(listing_title=name)
        Comment(title = title, comment = comments, commented_user = username).save()
        return render(request, "auctions/listing.html",{
            "title" : ActiveListing.objects.get( listing_title=name),
            "comments" : ActiveListing.objects.get(listing_title=name).comments.all(),
        })
    return render(request, "auctions/listing.html",{
        "title" : ActiveListing.objects.get(listing_title=name),
        "comments" : ActiveListing.objects.get(listing_title=name).comments.all(),
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
