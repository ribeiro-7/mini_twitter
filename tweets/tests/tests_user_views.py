from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse

class UserViewsTests(TestCase):

    #cria um usuário autenticado para fazer as requisições
    def authenticated_user(self):
        self.user = User.objects.create_user(username="test_user", password='123456')
        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=self.user)



    #teste de registro de usuario
    def test_user_register(self):

        data = {

            'email': 'usuario_teste@gmail.com',
            'username': 'user_teste',
            'password': '1234'

        }

        response = self.client.post('/user/register/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='user_teste').exists())


    #teste para logar usuario
    def test_login_user(self):

        username = 'usuario_teste'
        password = '1234'
        User.objects.create_user(username=username, password=password)

        data = {
            'username': 'usuario_teste',
            'password': '1234'
        }

        response = self.client.post('/user/login/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


    #teste para mostrar o perfil do usuario logado
    def test_profile_user_authenticated(self):

        self.authenticated_user()

        response = self.authenticated_client.get('/user/profile/')
        self.assertEqual(response.status_code, 200)

    #teste para mostrar o perfil
    def test_profile_user_unauthorized(self):

        response = self.client.get('/user/profile/')
        self.assertEqual(response.status_code, 401)


    #teste para token refresh
    def test_refresh_authenticated(self):

        User.objects.create_user(username='usuario_teste', password='1234')

        login_data = {
            'username': 'usuario_teste',
            'password': '1234'
        }

        login_response = self.client.post('/user/login/', login_data, format='json')

        self.assertEqual(login_response.status_code, 200)
        self.assertIn('refresh', login_response.data)

        refresh_token = login_response.data['refresh']
        refresh_data = {'refresh': refresh_token}

        refresh_response = self.client.post('/user/refresh/', refresh_data, format='json')

        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn('access', refresh_response.data)

    
    #teste para logout de usuario
    def test_user_logout_authenticated(self):
        client = APIClient()

        User.objects.create_user(username='usuario_teste', password='1234')

        login_data = {
            'username': 'usuario_teste',
            'password': '1234'
        }

        login_response = client.post('/user/login/', login_data, format='json')

        self.assertEqual(login_response.status_code, 200)
        self.assertIn('refresh', login_response.data)
        self.assertIn('access', login_response.data)

        refresh_token = login_response.data['refresh']
        access_token = login_response.data['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        refresh_data = {'refresh': refresh_token}

        logout_response = client.post('/user/logout/', refresh_data, format='json')

        self.assertEqual(logout_response.status_code, 205)
        self.assertEqual(logout_response.data["detail"], "Usuário deslogado com sucesso!")


    #teste para delete de usuario 
    def test_delete_user_authenticated(self):
        self.authenticated_user()

        response = self.authenticated_client.delete('/user/delete/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(username='usuario_teste').exists())
