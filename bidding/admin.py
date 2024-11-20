from django.contrib import admin
from .models import UserProfile, Auction

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'end_date', 'seller')
    search_fields = ('title', 'seller')
    list_filter = ('end_date', 'seller')

admin.site.register(UserProfile)
admin.site.register(Auction, AuctionAdmin)
