from django.urls import path
from .views import home, auction_list, auction_details, create_profile_view, place_bid_view, post_job_offer_view, register_view, order_post_view, profile_view, register_as_master

urlpatterns = [
    path('', home, name='home'),
    path('auctions/', auction_list, name='auction_list'),
    path('auctions/<int:id>/', auction_details, name='auction_details'),
    path('profile/create/', create_profile_view, name='create_profile'),
    path('auctions/<int:id>/bid/', place_bid_view, name='place_bid'),
    path('job/post/', post_job_offer_view, name='post_job_offer'),
    path('profile/register/', register_view, name='register_view'),  # Ensure this comes before the profile view
    path('order/post/', order_post_view, name='order_post_view'),
    path('profile/<str:username>/', profile_view, name='profile_view'),  # This should come after
    path('register-as-master/', register_as_master, name='register_as_master'),  # Added path for registering as master
]
