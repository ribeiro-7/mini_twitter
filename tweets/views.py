from django.shortcuts import render
from .models import Tweet
from .serializers import TweetIdSerializer, TweetSerializer
from rest_framework import viewsets, generics


class TweetView(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


#Lista o tweet de acordo com o id passado no url
class TweetIdView(generics.RetrieveAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetIdSerializer