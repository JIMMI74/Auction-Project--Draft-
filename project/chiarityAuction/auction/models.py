from django.db import models
# from django.contrib.auth.models import User
from accounts.models import Profile, User
from datetime import datetime

from django.utils import timezone


 # class User(User):
 #   def __str__(self):
#        return f"{self.first_name}"



    

class AuctionListing(models.Model):
    
    profile =models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    product = models.CharField(max_length=200)
    #photo = models.ImageField(blank=True,  null=True, upload_to='uploads/')
    slug=models.SlugField(max_length=200,db_index=True)
    photo = models.ImageField(upload_to="pics/%y/%m/%d/")
    description = models.TextField(max_length=500)
    starting_bid = models.FloatField(default=0.01)
    current_price = models.FloatField()
    current_winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_winner", blank=True, null=True)
    active = models.BooleanField(default=True)
    manualClose = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now, blank=True)
    start =  models.DateTimeField(blank=True)
    end =  models.DateTimeField(blank=True)   
     
    
        
    def __str__(self):
        return f"{self.product}: $ {self.current_price}: ${self.date}"


class Watchlist(models.Model):
   
    auction_listings = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='watchlist')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='watchlist')



class Bid(models.Model):
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="bids")
    value = models.FloatField()


class Comment(models.Model):
    date = models.DateField(auto_created=True, default=timezone.now())
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=500)


