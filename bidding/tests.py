from django.test import TestCase
from .models import Auction, UserProfile, Order
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone  # Import timezone

class AuctionModelTest(TestCase):

    def test_create_auction(self):
        auction = Auction.objects.create(
            title="Test Auction",
            description="This is a test auction",
            starting_bid=100,
            price=150,
            end_date=timezone.now() + timezone.timedelta(days=7),  # Use timezone-aware datetime
            seller=UserProfile.objects.create(user=User.objects.create(username="testuser"))
        )
        self.assertEqual(auction.title, "Test Auction")
        self.assertEqual(auction.starting_bid, 100)

class AuctionViewsTest(TestCase):

    def test_auction_list_view(self):
        response = self.client.get(reverse('auction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Auction List")

    def test_auction_details_view(self):
        user = User.objects.create(username="testuser")
        profile = UserProfile.objects.create(user=user)
        auction = Auction.objects.create(
            title="Test Auction",
            description="This is a test auction",
            starting_bid=100,
            price=150,
            end_date=timezone.now() + timezone.timedelta(days=7),  # Use timezone-aware datetime
            seller=profile
        )
        response = self.client.get(reverse('auction_details', args=[auction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Auction")

class UserProfileModelTest(TestCase):

    def test_create_user_profile(self):
        user = User.objects.create(username="testuser")
        profile = UserProfile.objects.create(user=user)
        self.assertEqual(profile.user.username, "testuser")

class OrderModelTest(TestCase):

    def test_create_order(self):
        order = Order.objects.create(
            name="Test Order",
            description="This is a test order",
            address="Test Address",
            price=100.0,
            created_at=timezone.now()  # Use timezone-aware datetime
        )
        self.assertEqual(order.name, "Test Order")
        self.assertEqual(order.price, 100.0)
