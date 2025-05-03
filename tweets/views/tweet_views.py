from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from profiles.models import Profile


#tweet de todos usuarios
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweetsGlobal(request):
    
    try:
        tweets = Tweet.objects.all().order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(tweets, request)
        serializer = TweetSerializer(result_page, many=True, context={'request': request})

        return paginator.get_paginated_response(serializer.data)
    
    except:
        return Response({'detail': 'Você não tem autorização para esse endpoint!'}, status=401)

#tweets somente de pessoas que você segue
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweetsForyou(request):

    user = request.user

    try:
        following_profiles = user.following.all()
        following_users = [profile.user for profile in following_profiles]

        tweets = Tweet.objects.filter(user__in=following_users).order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(tweets, request)

        serializer = TweetSerializer(result_page, many=True, context={'request': request})
        paginated_response = paginator.get_paginated_response(serializer.data)

        return paginated_response
    
    
    except:
        return Response({'detail': 'Você não tem autorização para esse endpoint!'}, status=401)


#fazer seu proprio tweet
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def createTweet(request):
    user = request.user
    content = request.data.get('content')
    image = request.data.get('image')

    #se o usuario tentar criar um tweet sem conteúdo ou imagem, é necesário pelo menos um dos dois campos
    if (not content or content.strip == '') and not image:
        return Response({'error': 'É necessário pelo menos um campo para criar um tweet'})

    tweet = Tweet.objects.create(
        user=user,
        content=content,
        image=image
    )

    serializer = TweetSerializer(tweet, many=False, context={'request': request})
    return Response(serializer.data)

#atualiza tweet
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateTweet(request, pk):
    user = request.user
    
    try:
        tweet = Tweet.objects.get(id=pk)

        #se um usuário tentar alterar o tweet de outro
        if tweet.user != user:
            return Response({'error': 'Você não tem permissão para editar esse tweet.'}, status=403)
        
        content = request.data.get('content', tweet.content)
        image = request.FILES.get('image', tweet.image)

        tweet.content = content
        tweet.image = image
        tweet.save()

        serializer = TweetSerializer(tweet, many=False, context={'request': request})
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

    #se o usuário tentar deletar tweet de outro usuário
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
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchTweets(request):
    try:
        query = request.query_params.get('q', '')
        tweets = Tweet.objects.filter(content__icontains=query).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True, context={'request': request})
        return Response(serializer.data)
    except:
        return Response({'detail': 'Você não tem autorização para esse endpoint!'}, status=401)