from django import forms
from django.contrib.auth.models import User  # Import User model
from .models import Auction, AuctionImage, Bid, UserProfile, UserProfileImage, Job, ServiceRequest, Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'description', 'address', 'image', 'price']

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_bid', 'price', 'end_date']

class AuctionImageForm(forms.ModelForm):
    class Meta:
        model = AuctionImage
        fields = ['image']

AuctionImageFormSet = forms.inlineformset_factory(Auction, AuctionImage, form=AuctionImageForm, extra=5, max_num=5)

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount',]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'email', 'bio', 'location', 'birth_date']

class UserProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfileImage
        fields = ['image']

UserProfileImageFormSet = forms.inlineformset_factory(UserProfile, UserProfileImage, form=UserProfileImageForm, extra=5, max_num=5)

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
