from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home, auction_list, auction_details, create_profile_view, place_bid_view,
    post_job_offer_view, register_view, order_post_view, profile_view,
    register_as_master, test_view, order_post_success, bid  # Add bid view import
)
import logging

logger = logging.getLogger(__name__)

def log_urlpatterns():
    urlpatterns = [
        path('', home, name='home'),
        path('auctions/', auction_list, name='auction_list'),
        path('auctions/<int:id>/', auction_details, name='auction_details'),
        path('profile/create/', create_profile_view, name='create_profile'),
        path('auctions/<int:id>/bid/', place_bid_view, name='place_bid'),
        path('job/post/', post_job_offer_view, name='post_job_offer'),
        path('profile/register/', register_view, name='register_view'),
        path('order/post/', order_post_view, name='order_post'),
        path('order/post/success/', order_post_success, name='order_post_success'),
        path('profile/<str:username>/', profile_view, name='profile_view'),
        path('register-as-master/', register_as_master, name='register_as_master'),
        path('test/', test_view, name='test_view'),
        path('bid/<int:id>/', bid, name='bid'),  # Update to include ID parameter
        path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    ]

    for pattern in urlpatterns:
        logger.info(f'URL pattern: {pattern}')

    return urlpatterns

urlpatterns = log_urlpatterns()
