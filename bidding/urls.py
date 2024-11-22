from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL pattern for bidding app
    path('auctions/', views.auction_list, name='auction_list'),
    path('auction/<int:id>/details/', views.auction_details, name='auction_details'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
]
