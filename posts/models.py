from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.IntegerField()
    likedBy = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

class Comments(models.Model):
    comment = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)