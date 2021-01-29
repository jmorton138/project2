from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min, Sum
from django.core.files.storage import FileSystemStorage

from .models import User, Listing, Watchlist, Bid, Category, Comments, Winner

def index(request):
    listings = Listing.objects.all()
    bids = Bid.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings, "bids": bids
    })

@login_required
def create(request): 
    if request.method == "GET":
        return render(request, "auctions/create.html")
    if request.method == "POST":
        if request.user.is_authenticated:
            author = User.objects.filter(username=User.username)
            item = request.POST["title"]
            details = request.POST["details"]
            starting_bid = request.POST["starting_bid"]
            category= str(request.POST["category"])
            author = request.user
            if request.FILES:
                uploaded = request.FILES
                image = uploaded['image']
            else:
                image = None
            #fs = FileSystemStorage()
            #image = fs.save(uploaded.name, uploaded)
            l = Listing(item=item, details=details, price=starting_bid, category=category, author=author, active =True, image=image)
            l.save()
            if not Category.objects.filter(category = category):
                c = Category(category=category)
                c.save()
                c.listings.add(l)
            elif Category.objects.filter(category = category):
                c = Category.objects.get(category = category)
                c.listings.add(l)           
            return render(request, "auctions/create.html")

def active(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    bids = Bid.objects.filter(item_id = listing_id)
    comments = Comments.objects.filter(item_id = listing_id)
    if request.method == "GET":
        if listing.active == True:
            if request.user.is_authenticated:
                user = request.user
                if Watchlist.objects.filter(item = listing.item, user=user):
                    watchlist = Watchlist.objects.filter(item = listing.item, user=user)
                    return render(request, "auctions/active_listing.html",{
                    "listing": listing, "bids": bids, "comments": comments, "watchlist": watchlist
                    })
                elif not Watchlist.objects.filter(item = listing.item, user=user):
                    return render(request, "auctions/active_listing.html",{
                    "listing": listing, "bids": bids, "comments": comments
                    })
            else:
                return render(request, "auctions/active_listing.html",{
                "listing": listing, "bids": bids, "comments": comments
                })
        if listing.active == False:
            if request.user.is_authenticated:
                user=request.user
                if Winner.objects.filter(item_id = listing.id):
                    winner = Winner.objects.get(item = listing)
                    if winner.user == user:
                        winning = "You have won this auction" 
                        return render(request, "auctions/closed_listing.html",{
                        "listing": listing, "bids": bids, "comments": comments, "message": "Auction closed now", "winning": winning
                    })
            return render(request, "auctions/closed_listing.html",{
            "listing": listing, "bids": bids, "comments": comments, "message": "Auction closed"
            })
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            if  Watchlist.objects.filter(item = listing.item, user = user):
                Watchlist.objects.get(item = listing.item, user = user).delete()
                items = Watchlist.objects.filter(user=user)
                return render(request, "auctions/watchlist.html", {
                "items": items
                })
            else:
                item = Watchlist(watchlist_id = listing.id, item = listing.item, details = listing.details, price = listing.price, category = listing.category)
                item.save()
                item.user.add(user)
                items = Watchlist.objects.filter(user=user)
                return render(request, "auctions/watchlist.html", {
                "items": items
                })


@login_required
def close(request, listing_id):
    comments = Comments.objects.filter(item_id = listing_id)
    bids = Bid.objects.filter(item_id = listing_id)
    if request.method =="POST":
        bids = Bid.objects.filter(item_id = listing_id)
        listing = Listing.objects.get(id = listing_id)
        if request.user.is_authenticated:
            user = request.user
            if user == listing.author:
                #store user with highest bid as variable
                highest_bid = Bid.objects.filter(item_id = listing.id).aggregate(Max('bid'))
                highest_bid = highest_bid.get('bid__max')  
                if highest_bid == None:
                    highest_bid = listing.price
                    listing.active = False
                    listing.save()
                    return render(request, "auctions/closed_listing.html", {
                    "winner": "No winner", "message": "Auction closed", "listing": listing, "comments": comments, "highest_bid": highest_bid
                })
                elif highest_bid is not None:
                    highest_bid = float(highest_bid)
                for bid in bids:
                    final_bid = bid.bid
                    if final_bid == highest_bid:
                        winner = bid.user
                        w=Winner(item_id = listing.id, user=winner, winner= winner)
                        w.save()
                listing.active = False
                listing.save()
                return render(request, "auctions/closed_listing.html", {
                    "winner": winner, "message": "Auction closed", "listing": listing, "comments": comments, "highest_bid": highest_bid
                })
            else:
                return HttpResponseRedirect(reverse("active", args =(listing.id,)))


def categories(request):
    listings = Listing.objects.all()
    categories= Category.objects.all()
    return render(request, "auctions/categories.html", {
        "listings": listings, "categories": categories
    })


def category(request, category):
    if request.method =="GET":
        items = Listing.objects.filter(category= category)
        category = Category.objects.get(category = category)
        return render(request, "auctions/category_items.html", {
        "items": items
        })

@login_required
def comment(request, listing_id):
    if request.method=="POST":
        listing = Listing.objects.get(id = listing_id)
        if request.user.is_authenticated:
            user=request.user
            comment = request.POST["comment"]
            c = Comments(text=comment, user=user,item_id = listing.id)
            c.save()
            #listings = Listing.objects.filter(id=listing.id)
            #comments = Comments.objects.all()
            return HttpResponseRedirect(reverse("active", args =(listing.id,)))


@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    user=request.user
    if request.method == "POST":
        bid = float(request.POST["bid"]) 
        #compare bid to price
        #find highest bid and set to a variable
        highest_bid = Bid.objects.filter(item_id = listing.id).aggregate(Max('bid'))
        highest_bid = highest_bid.get('bid__max')
        if highest_bid == None:
            if bid <= listing.price:
                return render(request, "auctions/error.html", {
                    "message": "Bid must be higher than current price and highest bid", "highest_bid": highest_bid
                })
            elif bid > listing.price:
                new_bid = Bid(item_id = listing.id, bid = bid, user=user)
                new_bid.save()
                listing.price = bid
                listing.save()
                bids = Bid.objects.filter(item_id = listing.id)
                return render(request, "auctions/active_listing.html", {
                    "message": "Bid successful", "listing": listing, "bids": bids
                })
        elif highest_bid is not None:
            highest_bid = float(highest_bid)
            if  bid > listing.price and bid > highest_bid:
                #listing.price = bid
                #listing.save()
                new_bid = Bid(item_id = listing.id, bid = bid, user=user)
                new_bid.save()
                listing.price = bid
                listing.save()
                bids = Bid.objects.filter(item_id = listing.id)
                return render(request, "auctions/active_listing.html", {
                    "message": "Bid successful", "listing": listing, "bids": bids
                })
            else:
                return render(request, "auctions/error.html", {
                    "message": "Bid must be higher than current price and highest bid", "highest_bid": highest_bid
                })


@login_required
def watchlist(request):
    if request.user.is_authenticated:
        user = request.user
        items= Watchlist.objects.filter(user = user)
        listings = Listing.objects.all()
        return render(request, "auctions/watchlist.html", {
        "items": items
        })
    else:
        return render(request, "auctions/error.html", {
        "message": "Must be logged in"
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
