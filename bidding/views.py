from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Auction, Job, Bid, ServiceRequest
from .forms import BidForm, UserProfileForm, JobForm, UserRegistrationForm, ServiceRequestForm
from django.contrib.auth import login
from datetime import datetime
from django.http import JsonResponse
from django.core.mail import send_mail

# Home View
def home(request):
    return render(request, 'bidding/home.html')

# Register View
def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.role = 'guest'  # Set the role to guest for new registrations
            profile.save()
            return redirect('profile', username=user.username)
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    return render(request, 'bidding/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# Order Post View
def order_post_view(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user  # Assuming you have user authentication set up
            service_request.save()
            # Optionally send an email notification
            send_mail(
                'New Service Request',
                'A new service request has been submitted.',
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ServiceRequestForm()
    return render(request, 'bidding/order_post.html', {'form': form})

def order_post_success(request):
    return render(request, 'bidding/order_post_success.html')

# Post Job Offer View
def post_job_offer_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.poster = request.user  # Set the poster to the current user
            job.save()
            return redirect('auction_list')
    else:
        form = JobForm()
    return render(request, 'bidding/post_job_offer.html', {'form': form})

# Profile View
def profile_view(request, username):
    try:
        user_profile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return render(request, 'bidding/profile_not_found.html', {'username': username})

    jobs = Job.objects.filter(poster=user_profile)
    bids = Bid.objects.filter(bidder_name=user_profile.user.username)
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
@login_required
def place_bid_view(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.auction = auction
            bid.user = request.user
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
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile', username=request.user.username)
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
    return render(request, 'bidding/register_as_master.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# Protected Test View
@login_required
def test_view(request):
    return render(request, 'bidding/test.html')
