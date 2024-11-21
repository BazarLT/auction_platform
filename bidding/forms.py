from django import forms
from .models import Auction, Bid, UserProfile, Job

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'price', 'end_date']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount', 'bidder_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date', 'profile_picture']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'start_price', 'end_date']
