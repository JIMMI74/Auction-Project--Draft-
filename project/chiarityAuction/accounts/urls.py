from django.urls import path, include
from .views import registration_view, edit_profile,user_profile



urlpatterns = [
    path('registration/', registration_view, name='registration_view'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('user/<str:username>/', user_profile, name='user_profile'),
    
    
    

]
