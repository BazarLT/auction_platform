from django import forms
from .models import Auction, AuctionImage, Bid, UserProfile, UserProfileImage, ServiceRequest, Message
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Žinutė"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'starting_bid', 'price', 'end_date']

    def __init__(self, *args, **kwargs):
        super(AuctionForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Pavadinimas"
        self.fields['description'].label = "Aprašymas"
        self.fields['starting_bid'].label = "Pradinė kaina"
        self.fields['price'].label = "Kaina"
        self.fields['end_date'].label = "Pabaigos data"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class AuctionImageForm(forms.ModelForm):
    class Meta:
        model = AuctionImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(AuctionImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = "Nuotrauka"
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        if not image and not self.instance.pk:
            raise forms.ValidationError('Either an existing image must be kept or a new image uploaded.')
        return cleaned_data


AuctionImageFormSet = forms.inlineformset_factory(
    Auction, AuctionImage, form=AuctionImageForm, extra=3, max_num=3, can_delete=True
)

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount', 'bid_type']

    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['bid_amount'].label = "Statymo suma"
        self.fields['bid_type'].label = "Statymo tipas"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'email', 'bio', 'location', 'birth_date']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].label = "Telefonas"
        self.fields['email'].label = "El. paštas"
        self.fields['bio'].label = "Apie mane"
        self.fields['location'].label = "Vieta"
        self.fields['birth_date'].label = "Gimimo data"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfileImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(UserProfileImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = "Nuotrauka"
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})

UserProfileImageFormSet = forms.inlineformset_factory(UserProfile, UserProfileImage, form=UserProfileImageForm, extra=2, max_num=2)

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Vartotojo vardas"
        self.fields['email'].label = "El. paštas"
        self.fields['password'].label = "Slaptažodis"
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
    SERVICE_TYPE_CHOICES = [
        ('mūrininkas', 'Mūrininkas'),
        ('elektrikas', 'Elektrikas'),
        ('darbininkas', 'Darbininkas'),
        ('dažytojas_dekoratorius', 'Dažytojas Dekoratorius'),
        ('santechnikas', 'Santechnikas'),
        ('mechanikas', 'Mechanikas'),
        ('buhalterinė_apskaita', 'Buhalterinė Apskaita'),
        ('IT_programuotojas', 'IT Programuotojas'),
        ('technikas', 'Technikas'),
        ('kitos_uzduotys', 'Kitos Užduotys'),
    ]

    service_type = forms.ChoiceField(choices=SERVICE_TYPE_CHOICES, label="Paslaugų tipas")
    name = forms.CharField(max_length=100, label="Vardas")
    phone = forms.CharField(max_length=15, label="Telefonas")
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.0, label="Pradinė kaina")

    class Meta:
        model = ServiceRequest
        fields = ['service_type', 'description', 'name', 'phone', 'email', 'address', 'starting_bid']

    def __init__(self, *args, **kwargs):
        super(ServiceRequestForm, self).__init__(*args, **kwargs)
        self.fields['description'].label = "Aprašymas"
        self.fields['email'].label = "El. paštas"
        self.fields['address'].label = "Adresas"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
