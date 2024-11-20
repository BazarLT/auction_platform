from django.contrib import admin
from django.urls import path, include
from bidding import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Root URL pattern
    path('auctions/', views.auction_list, name='auction_list'),
    path('auction/<int:id>/details/', views.auction_details, name='auction_details'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
]
