import re
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Auction, UserProfile, ServiceRequest, AuctionImage

class AuctionModelTest(TestCase):

    def test_create_auction(self):
        user = User.objects.create(username="testuser")
        profile = UserProfile.objects.create(user=user)
        auction = Auction.objects.create(
            title="Test Auction",
            description="This is a test auction",
            starting_bid=100,
            price=150,
            end_date=timezone.now() + timezone.timedelta(days=7),
            seller=profile
        )
        self.assertEqual(auction.title, "Test Auction")
        self.assertEqual(auction.starting_bid, 100)

class AuctionImageModelTest(TestCase):

    def test_create_auction_image(self):
        user = User.objects.create(username="testuser")
        profile = UserProfile.objects.create(user=user)
        auction = Auction.objects.create(
            title="Test Auction",
            description="This is a test auction",
            starting_bid=100,
            price=150,
            end_date=timezone.now() + timezone.timedelta(days=7),
            seller=profile
        )
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        auction_image = AuctionImage.objects.create(auction=auction, image=image)
        self.assertEqual(auction_image.auction.title, "Test Auction")

class AuctionViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_auction_list_view(self):
        profile = UserProfile.objects.create(user=self.user)
        auction = Auction.objects.create(
            title="Test Auction",
            description="This is a test auction",
            starting_bid=100,
            price=150,
            end_date=timezone.now() + timezone.timedelta(days=7),
            seller=profile
        )
        response = self.client.get(reverse('auction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Auction")

    def test_auction_details_view(self):
        profile = UserProfile.objects.create(user=self.user)
        auction = Auction.objects.create(
            title="Test Auction",
            description="This is a test auction",
            starting_bid=100,
            price=150,
            end_date=timezone.now() + timezone.timedelta(days=7),
            seller=profile
        )
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        AuctionImage.objects.create(auction=auction, image=image)
        response = self.client.get(reverse('auction_details', args=[auction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Auction")

        # Use regex to match the dynamic image URL
        image_pattern = re.compile(r'<img src="/media/auction_images.test_image_\w+.jpg" alt="Test Auction Image">')
        self.assertRegex(response.content.decode(), image_pattern)

class UserProfileModelTest(TestCase):

    def test_create_user_profile(self):
        user = User.objects.create(username="testuser")
        profile = UserProfile.objects.create(user=user)
        self.assertEqual(profile.user.username, "testuser")

class ServiceRequestModelTest(TestCase):

    def test_create_service_request(self):
        user = User.objects.create(username="testuser")
        order = ServiceRequest.objects.create(
            user=user,
            name="Test Order",
            description="This is a test order",
            address="Test Address",
            created_at=timezone.now()
        )
        self.assertEqual(order.name, "Test Order")
        self.assertEqual(order.address, "Test Address")
