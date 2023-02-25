from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db.models import CharField, Value
from .models import Ticket, Review, Profile, UserFollower
from django.contrib import messages
from django.db.models import Q

# Create your views here.

@login_required(login_url='signin')
def home(request):
    return render(request, "index.html")
    

def signup(request):
    
    if request.method == "POST":
        # You can get user entries by username = request.POST['username']
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confpassword = request.POST.get('confpassword')
        
        if password == confpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect("signup")
            else:
                new_user = User.objects.create_user(username, email, password)
                new_user.save()
                
                #log user in and redirect to settings page
                user_login = authenticate(username=username, password=password)
                auth.login(request, user_login)
                
                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                # return redirect("signup")
                return redirect('settings')
                
        else:
            messages.info(request, 'Password Not Matching')
            return redirect("signup")
    else:
        return render(request, "signup.html")

def signin(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            username = user.username
            return redirect('feed')
        
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
        
    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def signout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def add_review(request, pk):
    username = request.user.username
    ticket = Ticket.objects.get(title=pk)
    if request.method == 'POST':
        rating = request.POST['rating']
        user = User.objects.get(username=username)
        headline = request.POST['headline']
        body = request.POST['body']
        new_review = Review.objects.create(ticket=ticket, rating=rating, user=user, headline=headline, body=body)
        new_review.save()
        return redirect("feed")
    return render(request,  'tickets/add_review.html', context={"ticket": ticket})

@login_required(login_url='signin')
def add_ticket(request):
    username = request.user.username
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        user = User.objects.get(username=username)
        new_ticket = Ticket.objects.create(title=title, description=description, user=user, image=image)
        new_ticket.save()
        
        return redirect("feed")
    else:
        return render(request,  'tickets/add_ticket.html')

@login_required(login_url='signin')
def feed(request):
    ##
    
    reviews = get_users_viewable_reviews(request)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), 
        key=lambda post: post.time_created, 
        reverse=True
    )
    return render(request, 'tickets/feed.html', context={'posts': posts})


def get_users_viewable_reviews(request):
    # return Review.objects.filter(user = user)
    # return Review.objects.all()
    subscribed_users = UserFollower.objects.filter(user=request.user).values_list('followed_user', flat=True)
    return Review.objects.filter(user__in=subscribed_users)
        

def get_users_viewable_tickets(request):
    subscribed_users = UserFollower.objects.filter(user=request.user).values_list('followed_user', flat=True)
    return Ticket.objects.filter(user__in=subscribed_users)

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_tickets = Ticket.objects.filter(user=user_object.id)
    user_reviews = Review.objects.filter(user=user_object.id)
    user_ticket_length = len(user_tickets)
    user_review_length = len(user_reviews)
    
    user = pk
    follow = UserFollower.objects.filter(user=request.user).exists()
    # user_follow = UserFollower.objects.get(followed_by=followed_by, user=following)

    user_followers = len(user_object.followed_by.all())
    user_following = len(user_object.following.all())
    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_tickets': user_tickets,
        'user_ticket_length': user_ticket_length,
        'user_reviews': user_reviews,
        'user_review_length': user_review_length,
        'follow': follow,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'users/profile.html', context)
 

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        following = User.objects.get(username=request.POST['following'])
        followed_by = request.user
        
        if UserFollower.objects.filter(followed_user=following, user=followed_by).first():
            delete_follower = UserFollower.objects.get(followed_user=following, user=followed_by)
            delete_follower.delete()
            return redirect('/profile/' + following.username)
        else:
            new_follower = UserFollower.objects.create(followed_user=following, user=followed_by)
            new_follower.save()
            return redirect('/profile/' + following.username)
    else:
        return redirect("feed")

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        image = request.FILES.get('profileimg')
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        
        return redirect('settings')
    return render(request, 'users/setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def subscription(request):
    user_followers = request.user.followed_by.all()
    user_following = request.user.following.all()
    
    context = {
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'users/subscription.html', context)

@login_required(login_url='signin')
def search(request):

    if request.method == 'POST':
        username = request.POST['username']
        print(f"username: {username}")
        username_object = User.objects.get(username=username)
        

    return render(request, 'users/subscription.html', {'username_object': username_object})