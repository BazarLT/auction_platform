import re
from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'List all registered URLs'

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        for url_pattern in url_patterns:
            self.print_pattern(url_pattern)

    def print_pattern(self, url_pattern, prefix=''):
        if hasattr(url_pattern, 'url_patterns'):
            for pattern in url_pattern.url_patterns:
                self.print_pattern(pattern, prefix + url_pattern.pattern.regex.pattern)
        else:
            self.stdout.write(f'{prefix}{url_pattern.pattern.regex.pattern}')

