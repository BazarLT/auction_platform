from django import forms
from django.contrib.auth.models import User
from .models import Auction, Bid, UserProfile, Job, ServiceRequest, Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'description', 'address', 'image', 'price']

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_bid', 'price', 'end_date']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount', 'bidder_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'email', 'bio', 'location', 'birth_date', 'profile_picture']

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

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

class ServiceRequestForm(forms.ModelForm):
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.0)

    class Meta:
        model = ServiceRequest
        fields = ['service_type', 'description', 'name', 'phone', 'email', 'address', 'starting_bid']
