from django.contrib import admin
from .models import Ticket, Review, UserFollower, Profile

# Register your models here.

admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(UserFollower)
admin.site.register(Profile)