from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from profiles.models import Profile


#tweet de todos usuarios
@api_view(['GET'])
def tweetsGlobal(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)

#tweets somente de pessoas que você segue
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweetsForyou(request):
    user = request.user

    try:
        following_profiles = user.following.all()
        following_users = [profile.user for profile in following_profiles]

        tweets = Tweet.objects.filter(user__in=following_users).order_by('-created_at')

        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)
    
    except Profile.DoesNotExist:
        return Response({'detail': 'Esse perfil não existe!'}, status=404)


#fazer seu proprio tweet
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTweet(request):
    user = request.user
    data = request.data

    tweet = Tweet.objects.create(
        user=user,
        content=data['content'],
        image=request.FILES.get('image')
    )

    serializer = TweetSerializer(tweet, many=False)
    return Response(serializer.data)