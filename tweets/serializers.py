from rest_framework import serializers
from .models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content', 'image']


class TweetIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content', 'image']