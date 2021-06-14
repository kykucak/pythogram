from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Like


class LikeSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedIdentityField(view_name='user-detail')
    post = serializers.HyperlinkedIdentityField(view_name='post-detail')

    class Meta:
        model = Like
        fields = '__all__'


class PostSerializer(serializers.HyperlinkedModelSerializer):

    likes = LikeSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password',)


class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'last_login']

