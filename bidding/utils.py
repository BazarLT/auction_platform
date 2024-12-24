from django.core.mail import send_mail
from django.contrib.auth.models import User

def send_payment_confirmation(user, auction):
    subject = 'Payment Confirmation'
    message = f'Your payment for the auction "{auction.title}" has been received and confirmed. Thank you!'
    send_mail(subject, message, 'jobvital@gmail.com', [user.email], fail_silently=False)

def send_outbid_notification(previous_bid):
    try:
        user = previous_bid.bidder.user
        recipient_list = [user.email]
    except User.DoesNotExist:
        recipient_list = []

    subject = 'You Have Been Outbid!'
    message = f'Your bid of ${previous_bid.bid_amount} on {previous_bid.auction.title} has been outbid.'
    send_mail(subject, message, 'jobvital@gmail.com', recipient_list, fail_silently=False)

def send_auction_end_notification(auction):
    subject = 'Auction Ending Soon!'
    message = f'The auction for {auction.title} is ending soon. Place your final bids now!'
    recipient_list = [watch.user.email for watch in auction.watchlist_set.all()]
    send_mail(subject, message, 'jobvital@gmail.com', recipient_list, fail_silently=False)

def send_confirmation_notification(user, auction):
    subject = 'Auction Winner Confirmed'
    message = f'Congratulations! You have won the auction "{auction.title}".'
    send_mail(subject, message, 'jobvital@gmail.com', [user.email], fail_silently=False)

def process_fee_payment(fee, seller):
    # Placeholder for processing fee payment logic
    # For example, you could integrate with a payment gateway to transfer the fee amount
    pass
