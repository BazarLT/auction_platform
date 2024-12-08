from django.core.mail import send_mail
from django.contrib.auth.models import User

def send_outbid_notification(previous_bid):
    try:
        user = User.objects.get(username=previous_bid.bidder_name)
        recipient_list = [user.email]
    except User.DoesNotExist:
        recipient_list = []

    subject = 'You Have Been Outbid!'
    message = f'Your bid of ${previous_bid.bid_amount} on {previous_bid.auction.title} has been outbid.'
    send_mail(subject, message, 'jobvital@gmail.com', recipient_list, fail_silently=False)

def send_auction_end_notification(auction):
    subject = 'Auction Ending Soon!'
    message = f'The auction for {auction.title} is ending soon. Place your final bids now!'
    recipient_list = [user.email for user in auction.watchers.all()]  # Ensure we get user emails
    send_mail(subject, message, 'jobvital@gmail.com', recipient_list, fail_silently=False)
