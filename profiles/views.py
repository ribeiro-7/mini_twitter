from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import Profile

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def followRelation(request, username):
    try:
        target_user = User.objects.get(username=username)
        target_profile = Profile.objects.get(user=target_user)
        current_user = request.user

        if current_user in target_profile.followers.all():
            target_profile.followers.remove(current_user)
            return Response({'message': f'Você parou de seguir {username}'})
        else:
            target_profile.followers.add(current_user)
            return Response({'message': f'Você começou a seguir {username}'})
    except User.DoesNotExist:
        return Response({'error:' 'Usuário não encontrado'}, status=404)