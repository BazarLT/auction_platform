from django.shortcuts import render, get_object_or_404
from .models import UserProfile, Auction

def profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    return render(request, 'bidding/profile.html', {'user_profile': user_profile})

def auction_details(request, id):
    auction = get_object_or_404(Auction, id=id)
    return render(request, 'bidding/auction_details.html', {'auction': auction})

def auction_list(request):
    auctions = Auction.objects.all()
    return render(request, 'bidding/auction_list.html', {'auctions': auctions})

def home(request):
    return render(request, 'bidding/home.html')
