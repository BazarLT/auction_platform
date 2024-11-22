from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bidding.urls')),  # Includes URLs from the bidding app
]
