from django import forms
from django.contrib.auth.models import User  # Add this import statement
from .models import Auction, Bid, UserProfile, Job

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_bid', 'price', 'end_date']  # Added 'starting_bid'

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount', 'bidder_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'email', 'bio', 'location', 'birth_date', 'profile_picture']  # Added 'phone_number' and 'email'

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'start_price', 'end_date']
