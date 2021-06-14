from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth.models import User

from .serializers import PostSerializer, RegistrationSerializer, UserSerializer, UserAccountSerializer
from .utils import *


class PostViewSet(ViewSet):

    @user_active
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    @user_active
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response({
            "user": PostSerializer(post, context={"request": request}).data
        })

    @user_active
    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class UserViewSet(ViewSet):

    @user_active
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserAccountSerializer(queryset, many=True)
        return Response(serializer.data)

    @user_active
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserAccountSerializer(user)
        return Response(serializer.data)


class LikeAPIView(APIView):

    @user_active
    def put(self, request, pk):
        liked = like(request.user, pk)
        if liked:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "User's already liked it."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @user_active
    def delete(self, request, pk):
        unlike(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@user_active
def get_analytics(request):
    """Returns analytics aggregated by day for a specified date range"""
    # split "2021-06-12" by "-", transform it to int and to date
    try:
        date_from = str_date_to_date(request.GET.get('date_from'))
        date_to = str_date_to_date(request.GET.get('date_to'))
    except TypeError:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except AttributeError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    likes = Like.objects.filter(date_created__range=[date_from, date_to]).order_by('date_created')
    days = aggregate_likes_by_day(list(likes))

    return Response({
        "days": days
    })


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    @user_active
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })
