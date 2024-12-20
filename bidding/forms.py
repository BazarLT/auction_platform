from django import forms
from django.contrib.auth.models import User
from .models import Auction, AuctionImage, Bid, UserProfile, UserProfileImage, ServiceRequest

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_bid', 'price', 'end_date']

    def __init__(self, *args, **kwargs):
        super(AuctionForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class AuctionImageForm(forms.ModelForm):
    class Meta:
        model = AuctionImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(AuctionImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})

AuctionImageFormSet = forms.inlineformset_factory(Auction, AuctionImage, form=AuctionImageForm, extra=5, max_num=5)

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount', 'bid_type']

    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'email', 'bio', 'location', 'birth_date']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfileImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(UserProfileImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})

UserProfileImageFormSet = forms.inlineformset_factory(UserProfile, UserProfileImage, form=UserProfileImageForm, extra=5, max_num=5)

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'type': 'password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ServiceRequestForm(forms.ModelForm):
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.0)

    class Meta:
        model = ServiceRequest
        fields = ['service_type', 'description', 'name', 'phone', 'email', 'address', 'starting_bid']

    def __init__(self, *args, **kwargs):
        super(ServiceRequestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
