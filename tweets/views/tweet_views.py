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
    serializer = TweetSerializer(tweets, many=True, context={'request': request})
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

        serializer = TweetSerializer(tweets, many=True, context={'request': request})
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

#atualiza tweet
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateTweet(request, pk):
    user = request.user
    
    try:
        tweet = Tweet.objects.get(id=pk)

        if tweet.user != user:
            return Response({'error': 'Você não tem permissão para editar esse tweet.'}, status=403)
        
        content = request.data.get('content', tweet.content)
        image = request.FILES.get('image', tweet.image)

        tweet.content = content
        tweet.image = image
        tweet.save()

        serializer = TweetSerializer(tweet, many=False)
        return Response(serializer.data)

    except Tweet.DoesNotExist:
        return Response({'error': 'Tweet inexistente.'}, status=404)
    
#deleta tweet
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTweet(request, pk):
    user = request.user

    try:
        tweet = Tweet.objects.get(id=pk)
    except Tweet.DoesNotExist:
        return Response({'error': 'Tweet inexistente.'}, status=404)

    
    if tweet.user != user:
        return Response({'error': 'Você não pode excluir o tweet de outro usuário.'}, status=403)
        
    tweet.delete()
    return Response({'detail': 'Tweet deletado com sucesso.'}, status=204)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likeDislikeFunction(request, pk):
    
    user = request.user

    try:
        tweet = Tweet.objects.get(id=pk)
    except Tweet.DoesNotExist:
        return Response({'error': 'Tweet não encontrado'}, 404)
    
    if tweet.likes.filter(id=user.id).exists():
        tweet.likes.remove(user)
        return Response({'detail': 'Like removido!'}, status=204)
    else:
        tweet.likes.add(user)
        return Response({'detail': 'Like adicionado ao tweet!'}, status=204)


#usuario faz pesquisa por palavra-chave ou hashtag
api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchTweets(request):
    query = request.query_params.get('q', '')
    tweets = Tweet.objects.get(content__icontain=query).order_by('-created_at')
    serializer = TweetSerializer(tweets, many=True, context={'request': request})
    return Response(serializer.data)