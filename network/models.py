from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
            return f"{self.first_name} {self.last_name}"

class Post(models.Model):
    content = models.CharField(max_length=280)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    time_posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.poster} posts: '{self.content}'."

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user} likes the post {self.post}."

class Follower(models.Model):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_followed")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_following")

    def __str__(self):
        return f"{self.following_user} has started following {self.followed_user}."