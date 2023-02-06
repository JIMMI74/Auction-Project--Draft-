from django.contrib import admin
from accounts.models import Profile
from auction.models import AuctionListing, Bid, Comment, Watchlist


admin.site.register([  Bid, Comment, Watchlist])

@admin.register(AuctionListing)
class AuctionListingAdmin(admin.ModelAdmin):

    list_display = ('pk','product', 'description', 'current_price', 'date', 'active', 'profile','photo','slug','starting_bid', 'start','end')
    list_filter = ('product', 'description', 'current_price', 'date', 'active', 'profile')
    search_fields = ('product', 'description', 'current_price', 'date', 'active', 'profile')
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user')
    list_filter = ('user',)
    search_fields = ('user',)




""" @admin.unregister(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email', 'first_name', 'last_name') """