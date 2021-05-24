
from django.urls import path

from . import views

urlpatterns = [

    # API Routes
    path("follow_button", views.follow_button, name="follow_button"),
    path("like_button", views.like_button, name="like_button"),
    path("edit_button", views.edit_button, name="edit_button"),
    path("delete_button", views.delete_button, name="delete_button"),
    path("save_button", views.save_button, name="save_button"),

    # Site routes
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("not_found", views.not_found, name="not_found"),
    path("following", views.following, name="following"),
    path("<str:name>", views.profile_page, name="profile_page"),

    
]
