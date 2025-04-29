from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
def tweetsGlobal(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createTweet(request):
    user = request.user
    data = request.data

    tweet = Tweet.objects.create(
        user=user,
        content=data['content'],
        image=data['image']
    )

    serializer = TweetSerializer(tweet, many=False)
    return Response(serializer.data)