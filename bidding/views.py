from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Auction, ServiceRequest, UserProfile, UserProfileImage, AuctionImage, Bid, Watchlist, Message
from .forms import ServiceRequestForm, BidForm, UserRegistrationForm, UserProfileForm, UserProfileImageFormSet, AuctionForm, AuctionImageFormSet
from datetime import timedelta
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from .utils import send_outbid_notification
import smtplib

@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    bids = Bid.objects.filter(bidder=user_profile)
    watchlist = Watchlist.objects.filter(user=user_profile)
    messages = Message.objects.filter(receiver=user_profile)
    auctions = Auction.objects.filter(seller=user_profile)
    return render(request, 'bidding/profile.html', {
        'user_profile': user_profile,
        'bids': bids,
        'watchlist': watchlist,
        'messages': messages,
        'auctions': auctions,
    })

@login_required
def edit_profile(request, username):
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
        'user_profile': user_profile,
    })

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def home(request):
    return render(request, 'bidding/home.html')

@login_required
def auction_list(request):
    auctions = Auction.objects.all().prefetch_related('images')
    return render(request, 'bidding/auction_list.html', {'auctions': auctions})

@login_required
def auction_details(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    return render(request, 'bidding/auction_details.html', {'auction': auction})

@login_required
def place_bid_view(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            bid_type = form.cleaned_data['bid_type']
            previous_bid = Bid.objects.filter(auction=auction).order_by('-bid_time').first()
            bid = form.save(commit=False)
            bid.auction = auction
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            bid.bidder = user_profile
            bid.save()
            
            if bid_type == 'Up' and (previous_bid is None or bid_amount > previous_bid.bid_amount):
                auction.current_bid = bid_amount
                auction.save()
                if previous_bid:
                    send_outbid_notification(previous_bid)
                return redirect('auction_details', auction_id=auction.id)
            elif bid_type == 'Down' and (previous_bid is None or bid_amount < previous_bid.bid_amount):
                auction.current_bid = bid_amount
                auction.save()
                if previous_bid:
                    send_outbid_notification(previous_bid)
                return redirect('auction_details', auction_id=auction.id)
            else:
                form.add_error('bid_amount', 'Bid amount does not meet the criteria for the selected bid type.')
    else:
        form = BidForm()
    return render(request, 'bidding/place_bid.html', {'form': form, 'auction': auction})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        image_formset = UserProfileImageFormSet(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid() and image_formset.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            image_formset.instance = profile
            image_formset.save()
            user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            login(request, user)
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
        image_formset = UserProfileImageFormSet()
    return render(request, 'bidding/register.html', {'user_form': user_form, 'profile_form': profile_form, 'image_formset': image_formset})

@login_required
def post_auction(request):
    if request.method == 'POST':
        service_form = ServiceRequestForm(request.POST)
        formset = AuctionImageFormSet(request.POST, request.FILES)

        if service_form.is_valid() and formset.is_valid():
            service_request = service_form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            auction = Auction(
                title=service_request.service_type,
                description=service_request.description,
                starting_bid=service_form.cleaned_data['starting_bid'],
                current_bid=service_form.cleaned_data['starting_bid'],
                price=service_form.cleaned_data['starting_bid'],
                end_date=timezone.now() + timedelta(days=7),
                seller=user_profile
            )
            auction.save()
            formset.instance = auction
            formset.save()
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
            return redirect('auction_post_success')
        else:
            errors = service_form.errors

    else:
        service_form = ServiceRequestForm()
        formset = AuctionImageFormSet()

    return render(request, 'bidding/order_post.html', {
        'service_form': service_form,
        'formset': formset,
        'form_title': 'Post Service Request Auction',
        'form_description': 'Please fill out the form to post your service request auction.',
        'form_action': reverse('post_auction'),
        'form_button': 'Submit',
        'errors': errors if 'errors' in locals() else None,
    })

@login_required
def auction_post_success(request):
    return render(request, 'bidding/auction_post_success.html')

@login_required
def edit_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES, instance=auction)
        if form.is_valid():
            form.save()
            return redirect('auction_details', auction_id=auction.id)
    else:
        form = AuctionForm(instance=auction)
    return render(request, 'bidding/edit_auction.html', {'form': form, 'auction': auction})

@login_required
def delete_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if request.method == 'POST':
        auction.delete()
        return redirect('profile_view', username=request.user.username)
    return render(request, 'bidding/delete_auction.html', {'auction': auction})


@login_required
def watchlist_view(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, 'bidding/watchlist.html', {'watchlist_items': watchlist_items})

@login_required
def add_to_watchlist(request, auction_id):
    user_profile = UserProfile.objects.get(user=request.user)
    auction = get_object_or_404(Auction, id=auction_id)
    Watchlist.objects.get_or_create(user=user_profile, auction=auction)
    return redirect('watchlist_view')

@login_required
def remove_from_watchlist(request, auction_id):
    user_profile = UserProfile.objects.get(user=request.user)
    auction = get_object_or_404(Auction, id=auction_id)
    Watchlist.objects.filter(user=user_profile, auction=auction).delete()
    return redirect('watchlist_view')

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(UserProfile, id=receiver_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user.userprofile, receiver=receiver, content=content)
            return redirect('profile_view', username=receiver.user.username)
    return render(request, 'bidding/send_message.html', {'receiver': receiver})

@login_required
def view_messages(request):
    user_profile = UserProfile.objects.get(user=request.user)
    received_messages = Message.objects.filter(receiver=user_profile)
    sent_messages = Message.objects.filter(sender=user_profile)
    return render(request, 'bidding/view_messages.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })
@login_required
def confirm_winner(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if request.method == 'POST':
        # Calculate the fee (2% of the auction price)
        fee = auction.current_bid * 0.02

        # Process the fee payment
        process_fee_payment(fee, auction.seller)

        # Update the auction to set winner confirmed
        auction.winner_confirmed = True
        auction.save()

        # Send confirmation notification (email or message)
        send_confirmation_notification(request.user, auction)

        # Redirect to a success page or profile
        return redirect('profile_view', username=request.user.username)
    return render(request, 'bidding/confirm_winner.html', {'auction': auction})

