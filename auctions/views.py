from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })

@login_required(redirect_field_name='auctions/login.html')
def add(request):
    # Check if method is POST
    if request.method == "POST":

        # Accessing the user of auctions
        "TODO"

        # Finding title of listing
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]

        # Attempt to create new listing
        listing = Listing(title=title, description=description, price=price)
        listing.save()

        #Redirect user to list of tasks
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/add.html")

def bidding(request, listing_id):
    # For a post request, add a new bid (aka update bid)
    if request.method == "POST":

        # Accessing the listing
        listing = Listing.objects.get(pk=listing_id)

        # Finding the user id from the submitted form data
        bidder_id = request.POST["bidder"]

        # Finding the bidder based on the id
        bidder = User.objects.get(pk=bidder_id)

        # Access bid
        bid = request.POST["bid"]

        # Update current bid
        if bid > listing.price:
            listing.price = bid
            # Redirect user to listing page
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

        else:
            return render(request, "auctions/listing.html", {
                "message": "Invalid Bid"
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
