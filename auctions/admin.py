from django.contrib import admin
from .models import User, AuctionListing, Bid, Comment, Watchlist

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')


@admin.register(AuctionListing)
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_bid', 'current_price', 'category', 'status', 'created_at', 'created_by')
    search_fields = ('title', 'description', 'category')
    list_filter = ('status', 'category', 'created_at', 'created_by')


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'amount', 'timestamp')
    search_fields = ('user__username', 'auction__title')
    list_filter = ('timestamp', 'amount')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('auction', 'user', 'content', 'created_at')
    search_fields = ('user__username', 'auction__title', 'content')
    list_filter = ('created_at', 'user')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')
    search_fields = ('user__username', 'listing__title')
    list_filter = ('user',)
