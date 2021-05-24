from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
import json

from .models import User, Post, Like, Follower

def index(request):
    
    # Get objects
    posts = Post.objects.all().order_by('-time_posted')

    # Pagify objects
    p = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    # Get number of likes
    likes_total = total_likes(posts)

    # Get the likes for that user
    if (request.user):
        try:
            liked_posts = Like.objects.filter(user = request.user)
            liked_post_id_list = []
            for i in range(len(liked_posts)):
                liked_post_id_list.append(liked_posts[i].post.pk) 
        except:
            print("No user is logged in.")
            liked_post_id_list = []

    # Provide context
    context = {
        "posts": page,
        "likes": likes_total,
        "liked_posts": liked_post_id_list
    }

    return render(request, "network/index.html", context)


def total_likes(posts):

    # get all likes
    like_objects = Like.objects.all()

    # make likes into a searchable list
    likes = []
    for i in range(len(like_objects)):
        likes.append(like_objects[i].post.pk)
        
    # count how many times the post appears in the list
    total_likes = {}
    for i in range(len(posts)):
        number_of_likes = likes.count(posts[i].pk)
        total_likes[posts[i].pk] = number_of_likes

    return total_likes


def create_post(request):

    if request.method == "POST":

        # Get the data to create a post
        content = request.POST["content"]

        # Check character limit followed
        length = len(content)
        if (length == 0 or length > 280):
            return HttpResponseRedirect(reverse('index'))
        
        # Check valid user submitted
        if (request.user == None):
            return HttpResponseRedirect(reverse('index'))

        # Create a new post in database
        new_post = Post(content=content, poster=request.user)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))


def profile_page(request, name):
    
    # Check if user exists
    try:
        user_exists = User.objects.get(username = name)
    except:
        return HttpResponseRedirect(reverse('not_found'))

    # Get objects
    posts = Post.objects.filter(poster = user_exists)

    # Pagify objects
    p = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    # Get number of likes
    likes_total = total_likes(posts)

    # Get the likes for that user
    if (request.user):
        try:
            liked_posts = Like.objects.filter(user = request.user)
            liked_post_id_list = []
            for i in range(len(liked_posts)):
                liked_post_id_list.append(liked_posts[i].post.pk) 
        except:
            print("No user is logged in.")
            liked_post_id_list = []

    # Check if following user
    try:
        following = Follower.objects.get(followed_user = user_exists, following_user = request.user)
        follow_status = "unfollow"
        followed_user_id = user_exists.pk
    except:
        follow_status = "follow"
        followed_user_id = user_exists.pk

    follow_count = Follower.objects.filter(followed_user = user_exists).count()
    following_count = Follower.objects.filter(following_user = user_exists).count()

    # provide id's for the users
    
    following_user_id = request.user.pk

    # Provide context
    context = {
        "posts": page,
        "likes": likes_total,
        "liked_posts": liked_post_id_list,
        "username": user_exists.username,
        "follow_status": follow_status,
        "follow_count": follow_count,
        "following_count": following_count,
        "followed_user_id": followed_user_id,
        "following_user_id": following_user_id
    }

    return render(request, "network/profile_page.html", context)


@login_required(login_url='login')
def following(request):

    # Get objects 
    follow_list = Follower.objects.filter(following_user = request.user)

    length = len(follow_list)
    
    list_of_followed_users = []

    for i in range(length):
        list_of_followed_users.append(follow_list[i].followed_user)
        
    posts = Post.objects.filter(poster__in=list_of_followed_users).order_by('time_posted')

    # Pagify objects
    p = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    # Get number of likes
    likes_total = total_likes(posts)

    # Get the likes for that user
    if (request.user):
        try:
            liked_posts = Like.objects.filter(user = request.user)
            liked_post_id_list = []
            for i in range(len(liked_posts)):
                liked_post_id_list.append(liked_posts[i].post.pk) 
        except:
            print("No user is logged in.")
            liked_post_id_list = []

    # Provide context
    context = {
        "posts": page,
        "likes": likes_total,
        "liked_posts": liked_post_id_list
    }

    return render(request, "network/following.html", context)


def not_found(request):

    return render(request, "network/user_not_found.html")


def follow_button(request):
    
    # Following a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    json_data = json.load(request)
    follow_status = json_data['follow_status']
    followed_user_id = json_data['followed_user_id']
    following_user_id = json_data['following_user_id']
    followed_user = User.objects.get(pk = followed_user_id)
    following_user = User.objects.get(pk = following_user_id)

    if (follow_status == "unfollow"):
        # remove entry in database
        followed_entry = Follower.objects.get(followed_user = following_user, following_user = followed_user)
        followed_entry.delete()
        follow_status = "follow"
    else: # follow
        # create new entry in database
        new_entry = Follower(followed_user = following_user, following_user = followed_user)
        new_entry.save()
        follow_status = "unfollow"

    return JsonResponse({"follow_status": follow_status}, status=201)


def like_button(request):
    
    # Following a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    json_data = json.load(request)
    like_status = json_data['like_status']
    post_id = json_data['post_id']
    user = request.user
    post = Post.objects.get(pk = post_id)

    if (like_status == "unlike"):
        # remove entry in database
        liked_entry = Like.objects.get(post = post, user = user)
        liked_entry.delete()
        like_status = "like"
    else: # like
        # test if already exists
        liked_entry = Like.objects.filter(post = post, user = user)
        if (len(liked_entry) > 0):
            return JsonResponse({"like_status": like_status}, status=400)
        else:
            # create new entry in database
            new_entry = Like(post = post, user = user)
            new_entry.save()
            like_status = "unlike"

    return JsonResponse({"like_status": like_status}, status=201)


def edit_button(request):
    
    # Following a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    json_data = json.load(request)
    post_id = json_data['post_id']
    user = request.user
    post = Post.objects.get(pk = post_id)
    content = post.content

    return JsonResponse({"content_to_edit": content}, status=201)


def delete_button(request):
    
    # Following a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    json_data = json.load(request)
    post_id = json_data['post_id']
    post = Post.objects.get(pk = post_id)
    post.delete()

    return JsonResponse({"success": f"Post {post_id} deleted."}, status=201)


def save_button(request):
    
    # Following a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    json_data = json.load(request)
    post_id = json_data['post_id']
    updated_content = json_data['updated_content']

    print("Received the updated content as: ")
    print(updated_content)

    post = Post.objects.get(pk = post_id)

    print("Old content: ")
    print(post.content)

    post.content = updated_content

    print("Updated content: ")
    print(post.content)

    post.save()

    return JsonResponse({"success": f"Post {post_id} updated."}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
