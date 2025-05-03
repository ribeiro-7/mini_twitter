from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class UserModelTests(TestCase):

    def authenticated_user(self):
        self.user = User.objects.create_user(username="user_test", password="1234")
        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=self.user)


    #teste para registro de novo usuario
    def test_register_user(self):

        data = {

            'email': 'email_user_teste@gmail.com',
            'username': 'user_teste',
            'password': '1234'

        }


        self.client.post('/user/register/', data, format='json')

        self.assertTrue(User.objects.filter(username='user_teste').exists())


    #teste para delete de usuario 
    def test_delete_user_authenticated(self):

        self.authenticated_user()

        self.authenticated_client.delete('/user/delete/')
        self.assertFalse(User.objects.filter(username='usuario_teste').exists())