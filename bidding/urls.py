from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('', views.home, name='home'),
    path('auctions/', views.auction_list, name='auction_list'),
    path('auctions/<int:auction_id>/', views.auction_details, name='auction_details'),  # Changed `id` to `auction_id`
    path('auctions/<int:auction_id>/bid/', views.place_bid_view, name='place_bid'),
    path('register/', views.register, name='register'),
    path('post_auction/', views.post_auction, name='post_auction'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('auction/<int:auction_id>/edit/', views.edit_auction, name='edit_auction'),
    path('auction/<int:auction_id>/delete/', views.delete_auction, name='delete_auction'),
    path('auction/<int:auction_id>/confirm_winner/', views.confirm_auction_winner, name='confirm_winner'),  # Added path for confirming winner
    path('auction/<int:auction_id>/confirm_payment/', views.confirm_payment, name='confirm_payment'),  # Added path for confirming payment
    path('watchlist/', views.watchlist_view, name='watchlist_view'),
    path('watchlist/add/<int:auction_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:auction_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('messages/send/<int:receiver_id>/', views.send_message, name='send_message'),
    path('messages/', views.view_messages, name='view_messages'),
    path('auction_post_success/', views.auction_post_success, name='auction_post_success'),  # Ensure this line is included
    path('donation/', views.donation_page, name='donation_page'),  # Added donation_page path
    path('auction/<int:auction_id>/start_chat/', views.start_chat, name='start_chat'),  # Added start_chat path
    path('notifications/', views.view_notifications, name='view_notifications'),  # Added notifications path
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),  # Added mark as read path
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
