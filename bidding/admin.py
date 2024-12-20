from django.contrib import admin
from .models import UserProfile, Auction, UserProfileImage, AuctionImage, Bid, ServiceRequest, Watchlist, Message

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'end_date', 'seller')
    search_fields = ('title', 'seller')
    list_filter = ('end_date', 'seller')

# Removing JobAdmin since Job model no longer exists

admin.site.register(UserProfile)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(UserProfileImage)
admin.site.register(AuctionImage)
admin.site.register(Bid)
admin.site.register(ServiceRequest)
admin.site.register(Watchlist)
admin.site.register(Message)
