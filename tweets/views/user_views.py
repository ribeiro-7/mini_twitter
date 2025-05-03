from django.shortcuts import render
from rest_framework import status

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from tweets.serializers import UserSerializerWithToken, UserSerializer, MyTokenObtainPairSerializer


    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    
    data = request.data

    if User.objects.filter(email=data['email']).exists():
        return Response({'detail': 'Esse email já possui uma conta.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=data['username']).exists():
        return Response({'detail': 'Esse nome de usuário já está em uso.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create(
        email = data['email'],
        username = data['username'],
        password = make_password(data['password'])
    )

    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'detail': 'Usuário deslogado com sucesso!'}, status=205)
    except:
        return Response({'error': 'Token inválido ou expirado.'}, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    user = request.user
    user.delete()
    return Response("Usuário foi deletado com sucesso.", status=204)