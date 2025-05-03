from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Profile 

class ProfileTest(APITestCase):

    #usuarios para teste de relação
    def users_authenticated(self):

        self.follower = User.objects.create_user(username='seguidor', password='1234')
        self.target = User.objects.create_user(username='alvo', password='1234')
        self.target_profile = Profile.objects.get(user=self.target)

        self.client = APIClient()
        self.client.force_authenticate(user=self.follower)


    #teste de relação de follow e unfollow
    def test_follow_and_unfollow(self):
        self.users_authenticated()

        url = f'/profile/follow/{self.target.username}' 

        response_follow = self.client.post(url)

        self.assertEqual(response_follow.status_code, 200)
        self.assertIn(self.follower, self.target_profile.followers.all())
        self.assertEqual(response_follow.data['message'], f'Você começou a seguir {self.target.username}')

        self.target_profile.refresh_from_db()

        response_unfollow = self.client.post(url)
        self.assertEqual(response_unfollow.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.follower, self.target_profile.followers.all())
        self.assertEqual(response_unfollow.data['message'], f'Você parou de seguir {self.target.username}')
