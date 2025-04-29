from rest_framework import serializers
from .models import Tweet
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content', 'image', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)