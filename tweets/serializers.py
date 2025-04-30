from rest_framework import serializers
from .models import Tweet
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TweetSerializer(serializers.ModelSerializer):
    #pega o username do usuario para colocar no tweet
    username = serializers.CharField(source='user.username', read_only=True)
    #formata a data para o formato "dia de mês de ano - hora:minuto:segundo"
    created_at = serializers.DateTimeField(format="%d de %B de %Y - %H:%M:%S")

    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ['id', 'username', 'content', 'image', 'like_count', 'is_liked', 'created_at']


    def get_like_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and obj.likes.filter(id=user.id).exists()


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