
import pytest
import django
from django.conf import settings

def pytest_configure():
    settings.DEBUG = False
    django.setup()