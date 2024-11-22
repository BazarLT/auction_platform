from django.contrib import admin
from .models import UserProfile, Auction, Job

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'end_date', 'seller')
    search_fields = ('title', 'seller')
    list_filter = ('end_date', 'seller')

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_price', 'end_date', 'poster', 'status')
    search_fields = ('title', 'poster')
    list_filter = ('end_date', 'poster', 'status')

admin.site.register(UserProfile)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Job, JobAdmin)
