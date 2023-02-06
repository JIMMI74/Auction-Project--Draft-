from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=254, blank=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return "profile for user {}".format(self.user.username)
    
    

   
