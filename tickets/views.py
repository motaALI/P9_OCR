from itertools import chain

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.db.models import CharField, Q, Value
from django.shortcuts import redirect, render

from .models import Profile, Review, Ticket, UserFollower

# Create your views here.


def home(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        # You can get user entries by username = request.POST['username']
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confpassword = request.POST.get("confpassword")

        if password == confpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("home")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect("home")
            else:
                new_user = User.objects.create_user(username, email, password)
                new_user.save()

                # log user in and redirect to settings page
                user_login = authenticate(username=username, password=password)
                auth.login(request, user_login)

                # create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                # return redirect("signup")
                return redirect("settings")

        else:
            messages.info(request, "Password Not Matching")
            return redirect("signup")
    else:
        return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            username = user.username
            return redirect("feed")

        else:
            messages.info(request, "Credentials Invalid")
            return redirect("home")

    else:
        return render(request, "index.html")


@login_required(login_url="signin")
def signout(request):
    auth.logout(request)
    return render(request, "index.html")


@login_required(login_url="signin")
def add_review(request, pk):
    username = request.user.username
    ticket = Ticket.objects.get(title=pk)

    if request.method == "POST":
        if Review.objects.filter(ticket=ticket).exists():
            is_review_exist = (
                "Unable to create a review because the ticket has already been answered"
            )
            messages.warning(request, is_review_exist)
            post = Review.objects.get(ticket=ticket)
            return render(
                request, "tickets/review_snippet.html", context={"post": post}
            )

        rating = request.POST["rating"]
        user = User.objects.get(username=username)
        headline = request.POST["headline"]
        body = request.POST["body"]
        new_review = Review.objects.create(
            ticket=ticket, rating=rating, user=user, headline=headline, body=body
        )
        new_review.save()
        messages.success(request, "Review added successfully")
        return redirect("feed")
    return render(request, "tickets/add_review.html", context={"ticket": ticket})


@login_required(login_url="signin")
def add_ticket(request):
    username = request.user.username
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        user = User.objects.get(username=username)
        new_ticket = Ticket.objects.create(
            title=title, description=description, user=user, image=image
        )
        new_ticket.save()
        messages.success(request, "Ticket added successfully")
        return redirect("feed")
    else:
        return render(request, "tickets/add_ticket.html")


@login_required(login_url="signin")
def feed(request):
    ##

    reviews = get_users_viewable_reviews(request)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    for review in reviews:
        user_object = User.objects.get(username=review.user)
        user_profile = Profile.objects.get(user=user_object)
        review.user_photo_url = user_profile.image.url

    tickets = get_users_viewable_tickets(request)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    for ticket in tickets:
        user_object = User.objects.get(username=ticket.user)
        user_profile = Profile.objects.get(user=user_object)
        ticket.user_photo_url = user_profile.image.url

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )
    return render(request, "tickets/feed.html", context={"posts": posts})


def get_users_viewable_reviews(request):
    subscribed_users = UserFollower.objects.filter(user=request.user).values_list(
        "followed_user", flat=True
    )
    reviews = Review.objects.filter(Q(user=request.user) | Q(user__in=subscribed_users))
    return reviews


def get_users_viewable_tickets(request):
    subscribed_users = UserFollower.objects.filter(user=request.user).values_list(
        "followed_user", flat=True
    )
    tickets = Ticket.objects.filter(Q(user=request.user) | Q(user__in=subscribed_users))
    return tickets


@login_required(login_url="signin")
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_tickets = Ticket.objects.filter(user=user_object.id)
    user_reviews = Review.objects.filter(user=user_object.id)
    user_ticket_length = len(user_tickets)
    user_review_length = len(user_reviews)

    # user = pk
    follow = UserFollower.objects.filter(user=request.user).exists()
    # user_follow = UserFollower.objects.get(followed_by=followed_by, user=following)

    user_followers = len(user_object.followed_by.all())
    user_following = len(user_object.following.all())

    context = {
        "user_object": user_object,
        "user_profile": user_profile,
        "user_tickets": user_tickets,
        "user_ticket_length": user_ticket_length,
        "user_reviews": user_reviews,
        "user_review_length": user_review_length,
        "follow": follow,
        "user_followers": user_followers,
        "user_following": user_following,
    }
    return render(request, "users/profile.html", context)


@login_required(login_url="signin")
def follow(request):
    if request.method == "POST":
        following = User.objects.get(username=request.POST["following"])
        followed_by = request.user

        if UserFollower.objects.filter(
            followed_user=following, user=followed_by
        ).first():
            delete_follower = UserFollower.objects.get(
                followed_user=following, user=followed_by
            )
            delete_follower.delete()
            messages.info(request, "Unfollowing user succeeds")
            return redirect("/profile/" + following.username)
        else:
            new_follower = UserFollower.objects.create(
                followed_user=following, user=followed_by
            )
            new_follower.save()
            messages.info(request, "Following user succeeds")
            return redirect("/profile/" + following.username)
    else:
        return redirect("feed")


@login_required(login_url="signin")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        # Check if the form does not contain an image, take the default one
        if request.FILES.get("image") is None:
            image = user_profile.image
            bio = request.POST["bio"]
            location = request.POST["location"]
            user_profile.image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            messages.info(request, "Profile updated successfully without image")

        # Otherwise save this image
        if request.FILES.get("image") is not None:
            image = request.FILES.get("image")
            bio = request.POST["bio"]
            location = request.POST["location"]
            user_profile.image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            messages.info(request, "Profile updated successfully with image")
        return redirect("settings")

    user_profile = Profile.objects.get(user=request.user)

    return render(request, "users/setting.html", context={"user_profile": user_profile})


@login_required(login_url="signin")
def subscription(request):
    user_followers = request.user.followed_by.all()
    user_following = request.user.following.all()

    context = {
        "user_followers": user_followers,
        "user_following": user_following,
    }
    return render(request, "users/subscription.html", context)


@login_required(login_url="signin")
def search(request):
    if request.method == "POST":
        username = request.POST["username"]
        try:
            username_object = User.objects.get(username=username)
            return render(
                request, "users/subscription.html", {"username_object": username_object}
            )
        except User.DoesNotExist:
            useDoesNotExist = f"There is not a user with name : ({username})"
            messages.warning(request, useDoesNotExist)
            return render(
                request,
                "users/subscription.html",
                context={"useDoesNotExist": useDoesNotExist},
            )
