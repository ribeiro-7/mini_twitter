from django.urls import path
from tweets.views.tweet_views import *

urlpatterns = [
    path('global/', tweetsGlobal, name='global'),
    path('foryou/', tweetsForyou, name='Foryou'),
    path('create/', createTweet, name='create_tweet'),
    path('update/<int:pk>', updateTweet, name='update_tweet'),
    path('delete/<int:pk>', deleteTweet, name='delete_tweet'),
    path('<int:pk>/like', likeDislikeFunction, name='like-dislike'),
    path('search/', searchTweets, name='search_tweets')
]
