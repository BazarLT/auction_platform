from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Auction, ServiceRequest, UserProfile, UserProfileImage, AuctionImage, Bid, Order
from .forms import JobForm, ServiceRequestForm, BidForm, OrderForm, UserRegistrationForm, UserProfileForm, UserProfileImageFormSet, AuctionForm, AuctionImageFormSet
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from .utils import send_outbid_notification, send_auction_end_notification
import smtplib
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    jobs = user_profile.job_set.all()
    bids = Bid.objects.filter(bidder=user_profile)
    return render(request, 'bidding/profile.html', {
        'user_profile': user_profile,
        'jobs': jobs,
        'bids': bids,
    })

@login_required
def edit_profile(request, username):  # Ensure this function accepts 'username'
    user_profile = get_object_or_404(UserProfile, user__username=username)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        formset = UserProfileImageFormSet(request.POST, request.FILES, instance=user_profile)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('profile_view', username=user_profile.user.username)
    else:
        form = UserProfileForm(instance=user_profile)
        formset = UserProfileImageFormSet(instance=user_profile)
    return render(request, 'bidding/edit_profile.html', {
        'form': form,
        'formset': formset,
        'user_profile': user_profile
    })

@login_required
def test_view(request):
    return render(request, 'bidding/test.html')

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
    pass

@login_required
def place_bid_view(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            if bid_amount < auction.current_bid:
                if bid_amount >= 0:
                    previous_bid = Bid.objects.filter(auction=auction).order_by('-bid_time').first()
                    bid = form.save(commit=False)
                    bid.auction = auction
                    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                    bid.bidder = user_profile
                    bid.save()
                    auction.current_bid = bid_amount
                    auction.save()
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
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            auction = Auction(
                title=order.name,
                description=order.description,
                starting_bid=order.price,
                current_bid=order.price,
                price=order.price,
                end_date=timezone.now() + timedelta(days=7),
                seller=user_profile,
            )
            auction.save()
            return redirect('order_post_success')
    else:
        form = OrderForm()

    context = {
        'form': form,
        'form_title': 'Post Auction',
        'form_description': 'Please fill out the form to post your auction.',
        'form_action': reverse('order_post_view'),
        'form_button': 'Submit'
    }

    return render(request, 'bidding/post_offer.html', context)

@login_required
def post_auction(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)
        formset = AuctionImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            auction = form.save(commit=False)
            auction.seller = request.user.userprofile
            auction.save()
            formset.instance = auction
            formset.save()
            return redirect('auction_list')
    else:
        form = AuctionForm()
        formset = AuctionImageFormSet()
    return render(request, 'bidding/post_auction.html', {'form': form, 'formset': formset})

@login_required
def order_post_create(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            auction = Auction(
                title=service_request.service_type,
                description=service_request.description,
                starting_bid=form.cleaned_data['starting_bid'],
                current_bid=form.cleaned_data['starting_bid'],
                price=form.cleaned_data['starting_bid'],
                end_date=timezone.now() + timedelta(days=7),
                seller=user_profile
            )
            auction.save()
            try:
                send_mail(
                    'New Service Request',
                    'A new service request has been submitted.',
                    'from@example.com',
                    ['to@example.com'],
                    fail_silently=False,
                )
            except smtplib.SMTPAuthenticationError:
                pass
            return redirect('order_post_success')
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
def order_post_success(request):
    return render(request, 'bidding/order_post_success.html')

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'bidding/edit_order.html', {'form': form})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')
    return render(request, 'bidding/delete_order.html', {'order': order})
