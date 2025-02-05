from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_ROLES = (
        ('client', 'Client'),
        ('guest', 'Guest'),
        ('master', 'Master'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=USER_ROLES, default='guest')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    verification_badge = models.BooleanField(default=False)
    payment_info = models.CharField(max_length=255, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return self.user.username

class UserProfileImage(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return self.profile.user.username

class Auction(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateTimeField()
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    winner_confirmed = models.BooleanField(default=False)
    winner = models.ForeignKey(UserProfile, related_name='winning_auctions', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class AuctionImage(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='auction_images/')

    def __str__(self):
        return f"{self.auction.title} Image"

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    BID_TYPES = [('Up', 'Up'), ('Down', 'Down')]
    bid_type = models.CharField(max_length=10, choices=BID_TYPES, default='Up')

    def __str__(self):
        return f"{self.bidder.user.username} - {self.bid_amount} ({self.bid_type})"

class ServiceRequest(models.Model):
    SERVICE_TYPES = (
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
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    description = models.TextField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.service_type}'

class Watchlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user.username} - {self.auction.title}"

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.user.username} to {self.receiver.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.user.username} - {self.message}"
