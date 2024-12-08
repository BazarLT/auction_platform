from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Auction, ServiceRequest, UserProfile, Bid
from .forms import ServiceRequestForm, BidForm, OrderForm, UserRegistrationForm, UserProfileForm, AuctionForm
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from .utils import send_outbid_notification, send_auction_end_notification
import smtplib
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def home(request):
    return render(request, 'bidding/home.html')

@login_required
def auction_list(request):
    auctions = Auction.objects.all()
    for auction in auctions:
        if isinstance(auction.end_date, datetime):
            auction.end_date = auction.end_date.isoformat()
    return render(request, 'bidding/auction_list.html', {'auctions': auctions})

@login_required
def auction_details(request, id):
    auction = get_object_or_404(Auction, id=id)
    return render(request, 'bidding/auction_details.html', {'auction': auction})

@login_required
def create_profile_view(request):
    pass  # Implementation here

@login_required
def place_bid_view(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            if bid_amount < auction.current_bid:
                if bid_amount >= 0:  # Ensure bid is non-negative
                    previous_bid = Bid.objects.filter(auction=auction).order_by('-bid_time').first()
                    bid = form.save(commit=False)
                    bid.auction = auction
                    bid.bidder_name = request.user.username  # Assuming user is logged in
                    bid.save()

                    # Update the current bid price in the auction
                    auction.current_bid = bid_amount
                    auction.save()

                    # Send outbid notification
                    if previous_bid:
                        send_outbid_notification(previous_bid)

                    return redirect('auction_details', id=auction.id)
                else:
                    form.add_error('bid_amount', 'Bid amount must be non-negative.')
            else:
                form.add_error('bid_amount', 'Bid amount must be lower than the current bid.')
    else:
        form = BidForm()
    return render(request, 'bidding/place_bid.html', {'form': form, 'auction': auction})

@login_required
def post_job_offer_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_post_success')
    else:
        form = JobForm()
    return render(request, 'bidding/post_offer.html', {
        'form': form,
        'form_title': 'Post Job Offer',
        'form_description': None,
        'form_action': reverse('post_job_offer'),
        'form_button': 'Submit'
    })

def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            login(request, user)
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    return render(request, 'bidding/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def order_post_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            print(f"Order saved: {order}")  # Debug statement
            print(f"Uploaded image: {order.image}")  # Debug statement
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            auction = Auction(
                title=order.name,
                description=order.description,
                starting_bid=order.price,
                current_bid=order.price,
                price=order.price,
                end_date=timezone.now() + timedelta(days=7),
                seller=user_profile,
                image=order.image  # Save the uploaded image
            )
            auction.save()
            print(f"Auction saved: {auction}")  # Debug statement
            return redirect('order_post_success')
    else:
        form = OrderForm()
    
    # Create the context dictionary and verify the URL pattern name
    context = {
        'form': form,
        'form_title': 'Post Auction',
        'form_description': 'Please fill out the form to post your auction.',
        'form_action': reverse('order_post_view'),  # Ensure this URL name is correct
        'form_button': 'Submit'
    }
    
    print(context)  # Debug statement
    
    return render(request, 'bidding/post_offer.html', context)

@login_required
def order_post_create(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user  # Assuming you have user authentication set up
            service_request.save()

            # Create or get UserProfile
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)

            # Create a new Auction entry
            auction = Auction(
                title=service_request.service_type,
                description=service_request.description,
                starting_bid=form.cleaned_data['starting_bid'],
                current_bid=form.cleaned_data['starting_bid'],  # Initialize current bid
                price=form.cleaned_data['starting_bid'],
                end_date=timezone.now() + timedelta(days=7),  # Ensure timezone-aware datetime
                seller=user_profile
            )
            auction.save()

            # Optionally send an email notification
            try:
                send_mail(
                    'New Service Request',
                    'A new service request has been submitted.',
                    'from@example.com',
                    ['to@example.com'],
                    fail_silently=False,
                )
            except smtplib.SMTPAuthenticationError:
                pass  # Handle the email sending error if needed

            return redirect('order_post_success')  # Redirect to success page
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ServiceRequestForm()
    return render(request, 'bidding/post_offer.html', {
        'form': form,
        'form_title': 'Service Request',
        'form_description': None,
        'form_action': reverse('order_post_view'),
        'form_button': 'Submit'
    })

@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    jobs = user_profile.job_set.all()
    bids = user_profile.bid_set.all()
    return render(request, 'bidding/profile.html', {
        'user_profile': user_profile,
        'jobs': jobs,
        'bids': bids,
    })
