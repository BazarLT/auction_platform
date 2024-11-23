from django.urls import path
from . import views

urlpatterns = [
    path('', views.auction_list_view, name='auction_list'),
    path('auction/<int:id>/', views.auction_detail_view, name='auction_detail'),
    path('bid/<int:id>/', views.place_bid_view, name='place_bid'),
    path('profile/', views.create_profile_view, name='create_profile'),
    path('job/', views.post_job_offer_view, name='post_job_offer'),
]
