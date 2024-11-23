from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile, Auction, Job, Bid
from .forms import BidForm, UserProfileForm, JobForm
from datetime import datetime

def profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    return render(request, 'bidding/profile.html', {'user_profile': user_profile})

def auction_details(request, id):
    auction = get_object_or_404(Auction, id=id)
    
    if isinstance(auction.end_date, datetime):
        auction.end_date = auction.end_date.isoformat()
    
    return render(request, 'bidding/auction_details.html', {'auction': auction})

def auction_list(request):
    auctions = Auction.objects.all()
    
    for auction in auctions:
        if isinstance(auction.end_date, datetime):
            auction.end_date = auction.end_date.isoformat()
    
    return render(request, 'bidding/auction_list.html', {'auctions': auctions})

def home(request):
    return render(request, 'bidding/home.html')

# New Views for Bidding, Creating Profiles, and Posting Job Offers
def place_bid_view(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            # Handle placing bid logic
            bid = form.save(commit=False)
            bid.auction = auction
            bid.save()
            return redirect('auction_details', id=auction.id)
    else:
        form = BidForm()
    return render(request, 'bidding/place_bid.html', {'form': form, 'auction': auction})

def create_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('auction_list')
    else:
        form = UserProfileForm()
    return render(request, 'bidding/create_profile.html', {'form': form})

def post_job_offer_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auction_list')
    else:
        form = JobForm()
    return render(request, 'bidding/post_job_offer.html', {'form': form})
