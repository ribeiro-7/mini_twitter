from django.shortcuts import render
from rest_framework import status

from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from tweets.serializers import UserSerializerWithToken, UserSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        #tweets de todo mundo
        'tweets/global',
        #tweets das pessoas que o usuario segue
        'tweets/foryou',
        'user/register/',
        'user/login/',
        'user/profile/'
    ]
    return Response(routes)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            email = data['email'],
            username = data['username'],
            password = make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)

    except:
        message = {"Detail":"O usuário com este e-mail já está cadastrado"}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request, pk):
    userForDeletion = User.objects.delete(id = pk)
    userForDeletion.delete()
    return Response("O usuário foi deletado com sucesso.")


