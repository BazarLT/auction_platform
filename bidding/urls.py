from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # other URL patterns
    path('auction/<int:auction_id>/confirm_winner/', views.confirm_winner, name='confirm_winner'),
    path('', views.home, name='home'),
    path('auctions/', views.auction_list, name='auction_list'),
    path('auctions/<int:auction_id>/', views.auction_details, name='auction_details'),  # Changed `id` to `auction_id`
    path('auctions/<int:auction_id>/bid/', views.place_bid_view, name='place_bid'),
    path('register/', views.register, name='register'),
    path('post_auction/', views.post_auction, name='post_auction'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('users/', views.user_list, name='user_list'),
    path('auction/<int:auction_id>/edit/', views.edit_auction, name='edit_auction'),
    path('auction/<int:auction_id>/delete/', views.delete_auction, name='delete_auction'),
    path('watchlist/', views.watchlist_view, name='watchlist_view'),
    path('watchlist/add/<int:auction_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:auction_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('messages/send/<int:receiver_id>/', views.send_message, name='send_message'),
    path('messages/', views.view_messages, name='view_messages'),
    path('auction_post_success/', views.auction_post_success, name='auction_post_success'),  # Ensure this line is included
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
