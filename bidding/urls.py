from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    home, auction_list, auction_details, create_profile_view, place_bid_view,
    post_job_offer_view, register_view, order_post_view, profile_view, 
    order_post_success, test_view, user_list, edit_order, delete_order, edit_profile
)

urlpatterns =  [
    path('', home, name='home'),
    path('auctions/', auction_list, name='auction_list'),
    path('auctions/<int:id>/', auction_details, name='auction_details'),
    path('profile/create/', create_profile_view, name='create_profile'),
    path('auctions/<int:id>/bid/', place_bid_view, name='place_bid'),
    path('job/post/', post_job_offer_view, name='post_job_offer'),
    path('register/', register_view, name='register_view'),
    path('order/post/', order_post_view, name='order_post_view'),
    path('order/post/success/', order_post_success, name='order_post_success'),
    path('profile/<str:username>/', profile_view, name='profile_view'),
    path('profile/<str:username>/edit/', edit_profile, name='edit_profile'),  # Ensure the URL pattern includes username
    path('test/', test_view, name='test_view'),
    path('users/', user_list, name='user_list'),
    path('order/<int:order_id>/edit/', edit_order, name='edit_order'),
    path('order/<int:order_id>/delete/', delete_order, name='delete_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
