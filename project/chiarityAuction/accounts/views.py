from django.shortcuts import render, redirect, get_object_or_404,redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, UserEditForm
from .models import Profile
from auction.models import AuctionListing
from django.contrib.auth.models import User
from django.contrib import messages
from auction.models import Watchlist, AuctionListing






def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            Profile.objects.create(user=user)
            profile = Profile.objects.get(user=user)
            login(request, user)
            messages.success(request,
                             f'{profile.user}Your Account has been created successfully' 
                             f'You are now able to log in')
            return redirect("index")
    else:
        form = RegistrationForm()
    context = {"form": form}
    return render(request, "accounts/registration.html", context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    print(user, 'USER')
    profile = Profile.objects.get(user=request.user)
    print(profile, 'PROFILE')
    watchlist = Watchlist.objects.filter(user=request.user.pk).order_by('auction_listings_id')
    print(watchlist, 'OBJECTS')

    context = {"user": user, "profile": profile, "watchlist": watchlist}
    return render(request, 'accounts/user_profile.html', context)



 
  
 
  




def edit_profile(request):
    if request.method == 'POST':
        userform = UserEditForm(data=request.POST, instance=request.user)
        if userform.is_valid():
            userform.save()
            messages.success(request, ('You just edited your profile'))
            return redirect('/')
        else:
            messages.error(request, 'Check your data')
    else:
        print(request.user)
        print(request.user.profile)
        userform = UserEditForm(instance=request.user)

    context = {'userform': userform}
    return render(request, 'accounts/edit_profile.html', context)


def userWin(request):
    user = get_user_or404(request)
    print(user, 'USER')
    profile = Profile.objects.get(user=request.user)
    print(profile, 'PROFILE')
    winner = AuctionListing.objects.filter(current_winner=request.user.pk)
    print(winner, 'OBJECTS')

    context = {"user": user, "profile": profile, "winner": winner}
    return render(request, 'accounts/mywinner.html', context)


def createdAuction(request):
    user = get_user_or404(request)
    print(user, 'USER')
    profile = Profile.objects.get(user=request.user)
    print(profile, 'PROFILE')
    mycreated = AuctionListing.objects.filter(profile=request.user.pk)
    print(mycreated ,'OBJECTS')

    context = {"user": user, "profile": profile, "mycreated": mycreated}
    return render(request, 'accounts/mycreated.html', context)

def get_user_or404(request):
    try:
        return User.objects.get(pk=request.user.pk)
    except User.DoesNotExist:
        raise Http404("User does not exist")








