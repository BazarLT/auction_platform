from django.shortcuts import render, get_object_or_404, redirect  # Import necessary modules
from django.http import JsonResponse
from .models import Auction, ServiceRequest, UserProfile, Bid
from .forms import ServiceRequestForm, BidForm
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.utils import timezone  # Import timezone
import smtplib

def home(request):
    return render(request, 'bidding/home.html')

def auction_list(request):
    auctions = Auction.objects.all()
    for auction in auctions:
        if isinstance(auction.end_date, datetime):
            auction.end_date = auction.end_date.isoformat()
    return render(request, 'bidding/auction_list.html', {'auctions': auctions})

def auction_details(request, id):
    auction = get_object_or_404(Auction, id=id)
    return render(request, 'bidding/auction_details.html', {'auction': auction})

def create_profile_view(request):
    # Implementation here
    pass

def place_bid_view(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            if bid_amount < auction.current_bid:
                # Only accept bids lower than the current bid
                bid = form.save(commit=False)
                bid.auction = auction
                bid.bidder_name = request.user.username  # Assuming user is logged in
                bid.save()

                # Update the current bid price in the auction
                auction.current_bid = bid_amount
                auction.save()

                return redirect('auction_details', id=auction.id)
            else:
                form.add_error('bid_amount', 'Bid amount must be lower than the current bid.')
    else:
        form = BidForm()
    return render(request, 'bidding/place_bid.html', {'form': form, 'auction': auction})

def post_job_offer_view(request):
    # Implementation here
    pass

def register_view(request):
    # Implementation here
    pass

def order_post_view(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user  # Assuming you have user authentication set up
            service_request.save()

            # Create a new Auction entry
            auction = Auction(
                title=service_request.service_type,
                description=service_request.description,
                starting_bid=form.cleaned_data['starting_bid'],
                current_bid=form.cleaned_data['starting_bid'],  # Initialize current bid
                price=form.cleaned_data['starting_bid'],
                end_date=timezone.now() + timedelta(days=7),  # Ensure timezone-aware datetime
                seller=UserProfile.objects.get(user=request.user)
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
                # Handle the email sending error if needed
                pass

            return redirect('order_post_success')  # Redirect to success page
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ServiceRequestForm()
    return render(request, 'bidding/order_post.html', {'form': form})

def profile_view(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    return render(request, 'bidding/profile.html', {'profile': profile})

def bid(request, id):
    auction = get_object_or_404(Auction, id=id)  # Fetch the auction by ID
    return render(request, 'bidding/bid.html', {'auction': auction})

def register_as_master(request):
    # Implementation here
    pass

def test_view(request):
    # Implementation here
    pass

def order_post_success(request):
    return render(request, 'bidding/order_post_success.html')
