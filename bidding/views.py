from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Auction, ServiceRequest, UserProfile, UserProfileImage, AuctionImage, Bid, Watchlist, Message, Notification
from .forms import ServiceRequestForm, BidForm, UserRegistrationForm, UserProfileForm, UserProfileImageFormSet, AuctionForm, AuctionImageFormSet, MessageForm
from .utils import send_outbid_notification, send_payment_confirmation, process_fee_payment, send_confirmation_notification

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

# Add other views here like start_chat, view_notifications, etc.


def donation_page(request):
    return render(request, 'bidding/donation.html')

@login_required
def start_chat(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    seller_profile = auction.seller
    buyer_profile = request.user.userprofile

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = buyer_profile
            message.receiver = seller_profile
            message.save()
            messages.success(request, 'Message sent to the seller!')
            return redirect('auction_details', auction_id=auction.id)
    else:
        form = MessageForm()

    return render(request, 'bidding/start_chat.html', {
        'form': form,
        'auction': auction,
        'seller_profile': seller_profile,
        'buyer_profile': buyer_profile,
    })


@login_required
def confirm_payment(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if request.method == 'POST':
        auction.payment_confirmed = True
        auction.save()

        send_payment_confirmation(request.user, auction)

        messages.success(request, 'Payment confirmed. Thank you!')
        return redirect('profile_view', username=request.user.username)
    return render(request, 'bidding/confirm_payment.html', {'auction': auction})

@login_required
def profile_view(request, username):
    user = User.objects.get(username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    bids = Bid.objects.filter(bidder=user_profile)
    watchlist = Watchlist.objects.filter(user=user_profile)
    messages = Message.objects.filter(receiver=user_profile)
    notifications = Notification.objects.filter(user=user_profile).order_by('-timestamp')
    auctions = Auction.objects.filter(seller=user_profile)
    return render(request, 'bidding/profile.html', {
        'user_profile': user_profile,
        'bids': bids,
        'watchlist': watchlist,
        'messages': messages,
        'notifications': notifications,
        'auctions': auctions,
    })


@login_required
def edit_profile(request, username):
    user = User.objects.get(username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
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

            # Create a notification for the previous bidder
            if bid_type == 'Up' and (previous_bid is None or bid_amount > previous_bid.bid_amount):
                auction.current_bid = bid_amount
                auction.save()
                if previous_bid:
                    Notification.objects.create(
                        user=previous_bid.bidder,
                        message=f"Your bid has been outbid on auction: {auction.title}"
                    )
            elif bid_type == 'Down' and (previous_bid is None or bid_amount < previous_bid.bid_amount):
                auction.current_bid = bid_amount
                auction.save()
                if previous_bid:
                    Notification.objects.create(
                        user=previous_bid.bidder,
                        message=f"Your bid has been outbid on auction: {auction.title}"
                    )
            return redirect('auction_details', auction_id=auction.id)
        else:
            form.add_error('bid_amount', 'Bid amount does not meet the criteria for the selected bid type.')
    else:
        form = BidForm()
        form.initial['bid_amount'] = auction.current_bid
    return render(request, 'bidding/place_bid.html', {'form': form, 'auction': auction})


# Similarly, update the views for auction end and win confirmation
@login_required
def confirm_auction_winner(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if auction.seller != request.user.userprofile:
        messages.error(request, 'You are not authorized to confirm this auction.')
        return redirect('auction_details', auction_id=auction.id)

    if request.method == 'POST':
        winning_bid = Bid.objects.filter(auction=auction).order_by('-bid_time').first()
        if winning_bid:
            auction.winner = winning_bid.bidder
            auction.winner_confirmed = True
            auction.save()
            Notification.objects.create(
                user=winning_bid.bidder,
                message=f"Congratulations! You have won the auction: {auction.title}"
            )
            messages.success(request, 'Auction winner confirmed.')
            return redirect('auction_details', auction_id=auction.id)
    return render(request, 'bidding/confirm_auction_winner.html', {'auction': auction})


@login_required
def post_auction(request):
    errors = None

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
            messages.success(request, 'A new auction was posted')
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
        'errors': errors,
    })

@login_required
def auction_post_success(request):
    return render(request, 'bidding/auction_post_success.html')

@login_required
def edit_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    # Debug: Print seller and current user info
    print("Auction Seller:", auction.seller)
    print("Current User Profile:", request.user.userprofile)
    print("Current User:", request.user)

    if auction.seller != request.user.userprofile:
        messages.error(request, 'You are not authorized to edit this auction.')
        print("User is not authorized to edit this auction.")  # Debug: Print debug message
        return redirect('auction_details', auction_id=auction.id)
    else:
        print("User is authorized to edit this auction.")  # Debug: Print debug message

    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES, instance=auction)
        formset = AuctionImageFormSet(request.POST, request.FILES, instance=auction)
        if form.is_valid() and formset.is_valid():
            form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.auction = auction
                instance.save()
            formset.save_m2m()
            messages.success(request, 'Auction updated successfully.')
            return redirect('auction_details', auction_id=auction.id)
        else:
            messages.error(request, 'There was an error updating the auction. Please check the form and try again.')
            print("Form Errors:", form.errors)  # Debug: Print form errors
            print("Formset Errors:", formset.errors)  # Debug: Print formset errors
    else:
        form = AuctionForm(instance=auction)
        formset = AuctionImageFormSet(instance=auction)
    return render(request, 'bidding/edit_auction.html', {
        'form': form,
        'formset': formset,
        'auction': auction,
    })

@login_required
def delete_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if auction.seller.user != request.user:
        messages.error(request, 'You are not authorized to delete this auction.')
        return redirect('auction_details', auction_id=auction.id)

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
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user.userprofile).order_by('-timestamp')
    return render(request, 'bidding/notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user.userprofile)
    notification.is_read = True
    notification.save()
    messages.success(request, 'Notification marked as read.')
    return redirect('view_notifications')

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
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        message.delete()
        return redirect('profile_view', username=request.user.username)
    return redirect('profile_view', username=request.user.username)

