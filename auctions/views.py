from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import  Bid, Comment,AuctionListing, Watchlist,User
from decimal import Decimal
from .forms import ListingForm


def index(request):
    listings = AuctionListing.objects.filter(current_price__gt=0).order_by('-created_at')
    paginator = Paginator(listings, 10)  # 10 items per page
    page_number = request.GET.get('page')  # Get the 'page' parameter from the request
    listings = paginator.get_page(page_number)  # Get the relevant page
    return render(request, "auctions/index.html", {
        "listings": listings

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

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user  
            listing.current_price = listing.starting_bid  
            listing.save()
            return redirect('index') 
    else:
        form = ListingForm()
    
    return render(request, 'auctions/create_listing.html', {'form': form})
def active_listings(request):
    listings = AuctionListing.objects.filter(current_price__gt=0)  
    return render(request, "auctions/active_listings.html", {
        "listings": listings
    })
def listing_page(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    comments = listing.comments.all()
    watchlist_status = False
    if request.user.is_authenticated:
        watchlist_status = Watchlist.objects.filter(user=request.user, listing=listing).exists()  
    highest_bid = listing.bids.order_by('-amount').first()
    winner = None
    if listing.status == 'closed' and highest_bid:
        winner = highest_bid.user

   
    return render(request, "auctions/listingpage.html", {
        'listing': listing,
        'comments': comments,
        'highest_bid': highest_bid,
        'watchlist_status': watchlist_status,  
        'winner': winner,
    })



@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    if request.method == "POST":
        try:
            bid_amount = Decimal(request.POST.get("bid_amount"))
        except (TypeError, ValueError):
            messages.error(request, "Invalid bid amount.")
            return redirect('listing_page', listing_id=listing_id)

        highest_bid = listing.bids.order_by('-amount').first()
        if bid_amount < listing.starting_bid or (highest_bid and bid_amount <= highest_bid.amount):
            messages.error(request, "Bid must be higher than the current price.")
            return redirect('listing_page', listing_id=listing_id)

        Bid.objects.create(auction=listing, user=request.user, amount=bid_amount)
        listing.current_price = bid_amount
        listing.save()
        messages.success(request, "Bid placed successfully!")
    return redirect('listing_page', listing_id=listing_id)

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    if request.user != listing.created_by:
        return redirect('auction_detail', listing_id=listing_id)
    listing.status = 'closed'
    listing.save()
    return redirect('listing_page', listing_id=listing_id)

@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    if request.method == "POST":
        content = request.POST.get("content")
        Comment.objects.create(auction=listing, user=request.user, content=content)
    return redirect('listing_page', listing_id=listing_id)

@login_required
def update_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    if request.method == "POST":
        if "add" in request.POST:
            Watchlist.objects.get_or_create(user=request.user, listing=listing)
            messages.success(request, "Item added to your watchlist.")
        elif "remove" in request.POST:
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
            messages.success(request, "Item removed from your watchlist.")
    return redirect("listing_page", listing_id=listing_id)
def watchlist_view(request):
    if not request.user.is_authenticated:
        return redirect("login")  

    watchlist_items = Watchlist.objects.filter(user=request.user).select_related('listing')

    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items,
    })
def categories_list(request):
    categories = dict(AuctionListing.CATEGORIES)
    return render(request, 'auctions/categories_list.html', {'categories': categories})


def category_listings(request, category_name): 
    listings = AuctionListing.objects.filter(category=category_name, status='open')
    return render(request, 'auctions/category_listings.html', {'category_name': category_name, 'listings': listings})