from django.db import models
from django.contrib.auth.models import User

# Extending the User model with UserProfile
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
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    phone_number = models.CharField(max_length=15, blank=True)  # Added phone number field
    email = models.EmailField(blank=True)  # Added email field

    def __str__(self):
        return self.user.username

# Auction model
class Auction(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)  # Added starting_bid field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateTimeField()
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Bid model
class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder_name = models.CharField(max_length=200)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder_name} - {self.bid_amount}"

# Job model
class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateTimeField()
    poster = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='open')

    def __str__(self):
        return self.title
