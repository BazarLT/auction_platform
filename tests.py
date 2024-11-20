from django.test import TestCase
from .models import Auction

class AuctionModelTest(TestCase):

    def test_create_auction(self):
        auction = Auction.objects.create(
            title="Test Auction",
            description="This is a test",
            starting_bid=100
        )
        self.assertEqual(auction.title, "Test Auction")
        self.assertEqual(auction.starting_bid, 100)
