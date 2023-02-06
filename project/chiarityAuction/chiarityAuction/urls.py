"""chiarityAuction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from auction.views import index,create_listing, listing_view, edit_listing,watchlist, close_auction, set_bid, comment, my_wins,ListActiveView, cards_view, batchHttp
from accounts.views import userWin, createdAuction
#from auction.task import newbatch


urlpatterns = [
    path('', index, name='index'),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    
    path("listing_view/<int:id>/", listing_view, name="listing_view"),
    path("create_listing/", create_listing, name="create_listing"),
    path("edit_listing/<int:id>/", edit_listing, name="edit_listing"),
    path("watchlist/", watchlist, name="watchlist"),
    path("watchlist/<int:id>/", watchlist, name="watchlist"),
    path("active_listings/", ListActiveView.as_view(), name="active_listings"),
    path("close_auction/<int:id>/",close_auction, name="close_auction"),
    path("set_bid/<int:id>/",set_bid, name="set_bid"),
    path("comment/<int:id>/",comment, name="comment"),
    path("cards/",cards_view, name="cards"),
    path("my_wins/",my_wins, name="my_wins"),
    path("batch/",batchHttp, name="batch"),
    path("userwin/",userWin, name="mywinner"),
    path("createdAuction/",createdAuction, name="mycreated"),
    #path("new_batch/",newbatch, name="new_batch"),
    
  

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
