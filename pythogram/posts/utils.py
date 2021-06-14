from django.shortcuts import get_object_or_404

import datetime

from .models import Post, Like
from .serializers import LikeSerializer


def like(user, post_pk):
    """Add post like, if user's not liked it yet"""
    post = get_object_or_404(Post.objects.all(), pk=post_pk)
    like_, created = Like.objects.get_or_create(
        user=user,
        post=post,
    )
    if created:
        post.likes.add(like_)
    return created


def unlike(user, post_pk):
    """Removes post like, if user's already liked it"""
    post = get_object_or_404(Post.objects.all(), pk=post_pk)
    like_ = get_object_or_404(Like.objects.all(), user=user, post=post)

    post.likes.remove(like_)
    like_.delete()
    return True


def create_day(like_, request):
    """Returns day, filled with passed like"""
    like_serializer = LikeSerializer(instance=like_, context={"request": request})
    day = {
        "date": like_.date_created,
        "likes_details": [like_serializer.data]
    }
    return day


def user_active(func):
    """Decorator, that tracks user activity"""
    def wrapper(*args, **kwargs):
        try:
            user = args[1].user
        except IndexError:
            user = args[0].user
        user.last_login = datetime.datetime.now()
        user.save()
        result = func(*args, **kwargs)
        return result

    return wrapper


def aggregate_likes_by_day(likes, request):
    """Aggregate like objects by day to return it"""
    days = []
    first = True
    for like_ in likes:
        if first:
            day = create_day(like_, request)
            first = False
            continue

        if like_.date_created != day["date"]:
            day["likes_total"] = len(day["likes_details"])
            days.append(day)
            day = create_day(like_, request)
        else:
            like_serializer = LikeSerializer(instance=like_, context={"request": request})
            day["likes_details"].append(like_serializer.data)

        if likes.index(like_) == len(likes) - 1:
            day["likes_total"] = len(day["likes_details"])
            days.append(day)

    return days


def str_date_to_date(date):
    """Transform "2021-08-15" date to date object"""
    new_date = datetime.date(*[int(d) for d in date.split('-')])

    return new_date
