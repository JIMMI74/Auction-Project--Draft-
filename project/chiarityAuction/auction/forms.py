
from django import forms
from .models import AuctionListing



class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['product','photo','description','starting_bid','date', 'start', 'end'] # 'current_price',
        widgets= { 'start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                'end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
        
    



        
        
                  