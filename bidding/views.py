from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile, Auction, Job, Bid
from .forms import BidForm, UserProfileForm, JobForm, UserRegistrationForm
from django.contrib.auth import login
from datetime import datetime

# Home View
def home(request):
    return render(request, 'bidding/home.html')

# Register View
def register_view(request):
    return render(request, 'bidding/register.html')

# Order Post View
def order_post_view(request):
    return render(request, 'bidding/order_post.html')

# Post Job Offer View
def post_job_offer_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('auction_list')
    else:
        form = JobForm()
    return render(request, 'bidding/post_job_offer.html', {'form': form})

# Profile View
def profile_view(request, username):
    try:
        user_profile = UserProfile.objects.get(user__username=username)  # Corrected line
    except UserProfile.DoesNotExist:
        return render(request, 'bidding/profile_not_found.html', {'username': username})

    jobs = Job.objects.filter(user=user_profile.user)
    bids = Bid.objects.filter(user=user_profile.user)
    return render(request, 'bidding/profile.html', {'user_profile': user_profile, 'jobs': jobs, 'bids': bids})

# Auction Details View
def auction_details(request, id):
    auction = get_object_or_404(Auction, id=id)
    if isinstance(auction.end_date, datetime):
        auction.end_date = auction.end_date.isoformat()
    return render(request, 'bidding/auction_details.html', {'auction': auction})

# Auction List View
def auction_list(request):
    auctions = Auction.objects.all()
    for auction in auctions:
        if isinstance(auction.end_date, datetime):
            auction.end_date = auction.end_date.isoformat()
    return render(request, 'bidding/auction_list.html', {'auctions': auctions})

# Place Bid View
def place_bid_view(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.auction = auction
            bid.save()
            return redirect('auction_details', id=auction.id)
    else:
        form = BidForm()
    return render(request, 'bidding/place_bid.html', {'form': form, 'auction': auction})

# Create Profile View
def create_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('auction_list')
    else:
        form = UserProfileForm()
    return render(request, 'bidding/create_profile.html', {'form': form})

# Register as Master View
def register_as_master(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.role = 'master'
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'bidding/register_as_master.html', context)
