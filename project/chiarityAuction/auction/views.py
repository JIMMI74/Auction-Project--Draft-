from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseForbidden

from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
import os
from .models import AuctionListing, User, Bid, Comment, Watchlist
from accounts.models import Profile
from .forms import AuctionListingForm

from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import messages
from django.views.generic import ListView
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

from django.db import connection, transaction
from django.utils import timezone
from json import dumps
from zoneinfo import ZoneInfo
#from django.utils.safestring import mark_safe
# import json


        

def index(request):
    active_listings = AuctionListing.objects.filter(active=True).all()
    print(request.user.id, 'USER ID')
    
    return render(request, "auction/index.html", context={'active_listings': active_listings})
    

def create_listing(request):
    if request.method == "GET":
        return render(request, "auction/create_listing.html", {
            'form': AuctionListingForm()
        })
    if request.method == "POST":
        timezoneUser = ZoneInfo(request.META['TZ'])
        form = AuctionListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = AuctionListing()
            new_listing = form.save(commit=False)
            username = Profile.objects.get(user=request.user.pk)
            print(username,'USERNAME')
            new_listing.profile = username
            print (new_listing.profile,'AUTHOR')
            new_listing.current_price = form.cleaned_data['starting_bid']
            new_listing.description = form.cleaned_data['description']
            new_listing.product = form.cleaned_data['product']
            new_listing.photo = form.cleaned_data['photo']
            new_listing.date = form.cleaned_data['date'].replace(tzinfo=timezoneUser)
            new_listing.start= form.cleaned_data['start'].replace(tzinfo=timezoneUser)
            new_listing.end = form.cleaned_data['end'].replace(tzinfo=timezoneUser)
            if(new_listing.start > new_listing.end):
                messages.add_message(request=request, level=constants.ERROR, message='Start date must be before end date')
                return redirect('/create_listing')
            adesso = timezone.now()
            adesso.replace(minute=0 , second=0, microsecond=0)
            #adesso.replace(tzinfo=timezone)
            print(new_listing.start, 'START')
            print(adesso, 'NOW')
            if(new_listing.start > adesso):
                print('start e maggiore a adesso')
                new_listing.active = False
            new_listing.save()
            """ print(new_listing.author, 'AUHTOR')
            print(User)
            new_listing.current_price = form.starting_bid
            """
            form.save()
            return redirect('/')
        for error in form.errors.values():
            messages.add_message(request=request, level=constants.ERROR, message=error)

            
""" def listing_view(request, id):
    
    # profile= Profile.objects.get(user=id)    #user 
    profile= Profile.objects.get(user=request.user)
    #print(profile,'PROFILE')
    
    try:
     #listing = AuctionListing.objects.get(profile=request.user.pk)
        profile= Profile.objects.get(user=id)
        listing = AuctionListing.objects.get(profile=profile)
    except ObjectDoesNotExist:
        messages.error(request,"Object no present")
        return render(request,('auction/index.html'))
    comments = Comment.objects.filter(auction_listing=listing).order_by('date')
    return render(request, "auction/view.html", {
        'listing': listing,
        'comments': comments,
    })                        
def listing_view(request, id):
    profile= Profile.objects.get(user=request.user.pk)
    # profile= Profile.objects.get(user=request.user)
    print(profile,'PROFILE')
    listing = AuctionListing.objects.get(description=id)
    comments = Comment.objects.filter(auction_listing=listing).order_by('date')
    return render(request, "auction/view.html", {
        'listing': listing,
        'comments': comments,
    })    """         

def listing_view(request, id):
    profile= Profile.objects.get(user=request.user.pk)
    listing = AuctionListing.objects.get(id=id)
    if listing == None:
        messages.error(request,"Object no present")
        return render(request,('auction/index.html'))
    
    else:
        comments = Comment.objects.filter(auction_listing=listing).order_by('date')
    return render(request, "auction/view.html", {'listing': listing,'comments': comments,'profile':profile})
    
    
    
  #class ListingObjectListView(ListView):
        
    
    
def edit_listing(request, id):
    if request.method == 'GET':
        new_listing = AuctionListing.objects.get(id=id)
        assert new_listing.profile == Profile.objects.get(user=request.user.pk), HttpResponseForbidden()
        print(new_listing.profile, 'AUTHOR')
        if new_listing.active == True:
            form = AuctionListingForm(initial={
                
                'description': new_listing.description,   
            })
            messages.warning(request,"You can also change description.")
            return redirect(f'/listing_view/{new_listing.id}/')
        else:
            form = AuctionListingForm(initial={
                'product': new_listing.product,
                'photo': new_listing.photo,
                'description': new_listing.description,
                'starting_bid': new_listing.starting_bid,
            
                })
            return render(request, "auction/edit_listing.html", {'form': form, 'id':id})

    if request.method == 'POST':
        listing = AuctionListing.objects.get(id=id)
        listing.product = request.POST.get('product')
        listing.starting_bid = request.POST.get('starting_bid')
        listing.description = request.POST.get('description')
        listing.current_winner = listing.current_winner
        if len(request.FILES) == 0:
            listing.photo = listing.photo
        else:
            os.remove(listing.photo.path)
            listing.photo = request.FILES.get('photo')
        listing.save()
        
    
        messages.add_message(request, constants.SUCCESS, message="Listing updated.")
        return redirect(f'/listing_view/{listing.id}/')
    
def set_bid(request, id):
    if request.method == 'POST':
        bid = request.POST.get('bid')
        listing = AuctionListing.objects.get(id=id)
        if float(bid) <= listing.current_price:
            messages.add_message(request, constants.ERROR, message="Bid has to be greater than current price.")
            return redirect(f'/listing_view/{listing.id}/')
        listing.current_price = bid
        listing.current_winner = request.user
        listing.save()
        messages.add_message(request, constants.SUCCESS, message="Your bid has been placed!")
        return redirect(f"/listing_view/{listing.id}/")  # inserire condizioni nel caso float o importo basso // e add list // pulsante close auction
    return render(request, 'auction/view.html')



def close_auction(request, id):
    if request.method == 'POST': # no get ma Post tramite pulsante 
        listing = AuctionListing.objects.get(id=id)
        if listing.profile == Profile.objects.get(user=request.user.pk) and listing.active == True:
            listing.active = False
            listing.manualClose = True
            listing.save()
            return redirect(f"/listing_view/{listing.id}/")
        else:
            messages.warning(request, "You can't close this auction.")
            return redirect(f"/listing_view/{listing.id}/")
    return redirect('/')
  
        
        
def comment(request, id):
    if request.method == 'POST':
        listing = AuctionListing.objects.get(id=id)
        print(id, 'chi E?')
        text = request.POST.get("comment")
        print(request.POST)
        new_comment = Comment()
        new_comment.text = text
        new_comment.auction_listing = listing
        new_comment.author = Profile.objects.get(user=request.user.pk)
        new_comment.save()
        return redirect(f"/listing_view/{listing.id}/")
    #return htttResponseRedirect(reverse('listing_view', args=(id,)))


    

@login_required
def my_wins(request):
    if request.method == 'GET':
        winned_auctions = AuctionListing.objects.filter(active=False, current_winner=request.user.pk)
        return render(request, "auction/my_wins.html", {'winned_auctions': winned_auctions})
    
    



@login_required     # da sistemare 
def watchlist(request):
    #watchlist = Watchlist.objects.filter(user=request.user.pk).all()
    #print(watchlist,"OGGETTI")
    #listings = AuctionListing.objects.get(id=id)
    #user = get_object_or_404(User, user=request.user.pk)
    #print(user, 'USER')
    #profile = Profile.objects.get(user=request.user.pk)
   # print(profile, 'PROFILE')
    
    if request.method == 'GET':
        if request.GET.get('listing_id'):
            id=request.POST.get('listing_id')
            watchlist = Watchlist.objects.filter(user_id=request.user.pk, auction_listings_id=id).all()
            if watchlist:
                return HttpResponse('si')
            else: 
                return HttpResponse('no')
        else:
            watchlist = Watchlist.objects.filter(user=request.user.pk).all()
            if watchlist:
                return HttpResponse('oggetti presenti')
            else :
                return HttpResponse('no oggetti')
        
        
               
    else:
        if request.POST.get('listing_id'):
            id=request.POST.get('listing_id')
            watchlist = Watchlist.objects.filter(user_id=request.user.pk, auction_listings_id=id).all()
            listing = AuctionListing.objects.get(id=request.POST.get('listing_id'))
            print(231,{id,watchlist,listing},request.user.pk)
            if not watchlist:
                watchlist1 = Watchlist()
                watchlist1.user = Profile.objects.get(user=request.user.pk) 
                watchlist1.auction_listings = listing
                print(dir(watchlist1))
                print(watchlist1.user_id,watchlist1.auction_listings_id)
                watchlist1.save()
                return HttpResponse('oggetto aggiunto alla lista')
            else:
                messages.error(request,"Oggeto gia presente")
                return render(request,('auction/index.html'))
        
        else:
            messages.error(request,"Perror")
            return render(request,('auction/index.html'))
      
    return  HttpResponse("ok")
    
    
    
    


class ListActiveView(ListView):
    model = AuctionListing
    template_name = "auction/listAuctionActive.html"
    ordering = ['-date']
    


def cards_view(request):
    user = User.objects.filter(username=request.user.username).first()
    print(user,"USER VEDERE")
    # bid = Bid.objects.get(user=user)
    total_list = AuctionListing.objects.filter(id=request.user.pk)
    print(total_list,"TOTAL LIST")
    if total_list is None:
        return HttpResponse("No active auction")
    
    else:
        #description = str(total_list.description)[0:40] + ".."
        return render(request, "auction/cards.html", {
            "user":user,
            "item":total_list,
               #"description": description
            })


def batch():
    with connection.cursor() as cursor:
        try:
            print('in cursor........')
            #cursor.execute("UPDATE auction_auctionlisting SET active = true ")
            #cursor.execute("SELECT * FROM auction_auctionlisting WHERE  start <= datetime('now') and  datetime('now') >= end ")
            #cursor.execute("SELECT id,start FROM auction_auctionlisting ")
            #cursor.execute("SELECT  datetime('now') as now  ")
            #row = cursor.fetchall()
            #print(row)
            cursor.execute("UPDATE auction_auctionlisting SET active = ( start <= datetime('now') and  datetime('now') <= end ) where manualClose = False ")
            cursor.fetchall() # ritorno emelenti modificati 
            return True
        except:
            return False

def batchHttp():
    result = batch()
    if result :
        return HttpResponse("ok")
    else :
        return HttpResponse("error")
