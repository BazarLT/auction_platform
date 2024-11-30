from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bidding.urls')),  # Include all URLs from the bidding app
]
