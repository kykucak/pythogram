from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Post, Like
from .serializers import PostSerializer


def like(user, post_pk):
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        return False
    like_, created = Like.objects.get_or_create(
        user=user,
        post=post
    )
    if created:
        post.likes.add(like_)

    return created


def unlike(user, post_pk):
    """Removes post like, if user's already liked it"""
    try:
        post = Post.objects.get(pk=post_pk)
        like_ = Like.objects.get(user=user, post=post)
    except (Post.DoesNotExist, Like.DoesNotExist):
        return False

    post.likes.remove(like_)
    like_.delete()
    return True


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer


@api_view(['PATCH'])
def like_post(request, pk):
    liked = like(request.user, pk)

    return Response({"success": f"{liked}"})


@api_view(['PATCH'])
def unlike_post(request, pk):
    unliked = unlike(request.user, pk)

    return Response({"success": f"{unliked}"})
