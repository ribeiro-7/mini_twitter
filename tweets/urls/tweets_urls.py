from django.urls import path
from tweets.views.tweet_views import *

urlpatterns = [
    path('global/', tweetsGlobal, name='Global'),
    path('foryou/', tweetsForyou, name='Foryou'),
    path('create/', createTweet, name='create_tweet'),
]
