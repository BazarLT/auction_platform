from django.core.management.base import BaseCommand
from django.urls import resolve
from django.conf import settings

class Command(BaseCommand):
    help = 'Check URL patterns'

    def handle(self, *args, **kwargs):
        url_patterns = [
            '/',
            '/test_images/',
            '/media/profile_pics/test_image.jpg',
            '/media/auction_images/test_image.jpg',
        ]
        for url in url_patterns:
            try:
                match = resolve(url)
                self.stdout.write(f"URL '{url}' is resolved to: {match.view_name}")
            except Exception as e:
                self.stderr.write(f"URL '{url}' could not be resolved: {e}")
