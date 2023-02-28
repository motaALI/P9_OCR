from django.urls import path

from . import views

urlpatterns = [
    # path('', views.home, name="home"),
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("add_ticket/", views.add_ticket, name="add_ticket"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("add_review/<str:pk>", views.add_review, name="add_review"),
    path("follow/", views.follow, name="follow"),
    path("subscription/", views.subscription, name="subscription"),
    path("search/", views.search, name="search"),
    path("settings/", views.settings, name="settings"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
]
