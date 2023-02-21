from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime

User = get_user_model()
# Create your models here.
# Profile => user
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='ticket_images/')
    time_created = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f"Ticket: {self.title} ' | ' {self.user}"

class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=2048, blank=True)
    time_created = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f"Ticket: {self.ticket} created by: {self.user}"
    
class UserFollower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')
    
    def __str__(self):
        return f"{self.user} "
    
    class Meta:
        unique_together = ('user','followed_user')

   