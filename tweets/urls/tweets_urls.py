from django.urls import path
from tweets.views.tweet_views import *

urlpatterns = [
    path('tweets/global/', tweetsGlobal, name='Global')
]
