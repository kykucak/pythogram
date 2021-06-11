from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField("Like", related_name="related_post", null=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="related_like")
    date_created = models.DateTimeField(auto_now=True)
