from django.test import TestCase
from tweets.models import Tweet
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse


class TweetTests(TestCase):


    #cria um usuário autenticado para fazer as requisições
    def authenticated_user(self):
        self.user = User.objects.create_user(username="test_user", password='123456')
        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=self.user)


    #teste para criar o tweet completo
    def test_create_tweet_with_content_and_image_authenticated(self):

        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  
            content_type='image/jpeg'
        )

        data = {
            'content': 'Tweet teste com contéudo e imagem',
            'image': image
        }
        
        response = self.authenticated_client.post('/tweets/create/', data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tweet.objects.count(), 1)
        tweet = Tweet.objects.first()
        self.assertEqual(tweet.content, 'Tweet com conteúdo e imagem!')
        self.assertTrue(tweet.image)

    
    #test para criar tweet completo sem autorização
    def test_create_tweet_with_content_and_image_unauthorized(self):

        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  
            content_type='image/jpeg'
        )

        data = {
            'content': 'Tweet teste com contéudo e imagem sem autenticação',
            'image': image
        }
        
        response = self.cliente.post('/tweets/create/', data, format='multipart')
        self.assertEqual(response.status_code, 401)




    #teste para criar tweet apenas com contéudo
    def test_create_tweet_with_only_content_authenticated(self):
        data = {'content': 'Conteúdo válido'}
        response = self.authenticated_client.post('/tweets/create/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tweet.objects.count(), 1)



    #teste para criar tweet apenas com contéudo sem autorização
    def test_create_tweet_with_only_content_unauthorized(self):
        data = {'content': 'Conteúdo válido sem autenticação'}
        response = self.client.post('/tweets/create/', data, format='json')
        self.assertEqual(response.status_code, 401)

    

    #teste para criar tweet apenas com imagem
    def test_create_tweet_with_only_image_autheticated(self):
        
        #simulando um arquivo de imagem
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  
            content_type='image/jpeg'
        )

        data = {'image': image}
        response = self.authenticated_client.post('tweets/create/', data, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tweet.object.count(), 1)
        self.assertIsNotNone(Tweet.objects.first().image)



    #teste para criar tweet apenas com imagem sem autorização
    def test_create_tweet_with_only_image_unauthorized(self):
        
        #simulando um arquivo de imagem
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  
            content_type='image/jpeg'
        )

        data = {'image': image}
        response = self.client.post('tweets/create/', data, format='multipart')

        self.assertEqual(response.status_code, 401)


    #teste para criar tweet sem nenhum dos campos
    def test_create_tweet_without_content(self):
        data = {'content': ''}
        response = self.authenticated_client.post('tweets/create/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('É necessário fornecer conteúdo ou imagem.', response.data['error'])


    #teste para ver feed global autenticado
    def test_feed_global_authenticated(self):

        response = self.authenticated_client.get('tweets/global/')
        self.assertEqual(response.status_code, 200)

    
    #teste para ver feed global sem autorização
    def test_feed_global_unauthorized(self):

        response = self.client.get('tweets/global/')
        self.assertEqual(response.status_code, 401)

    
    #teste para ver feed for you autorizado
    def test_feed_for_you_authenticated(self):
        response = self.authenticated_client.get('tweets/foryou/')
        self.assertEqual(response.status_code, 200)


    #teste para ver feed for you sem autorização
    def test_feed_for_you_unauthorized(self):
        response = self.client.get('tweets/foryou/')
        self.assertEqual(response.status_code, 401)


    #teste para editar tweet autorizado
    def test_update_tweet_autenticated(self):

        tweet = Tweet.objects.create(user=self.authenticated_client, content="Teste editar tweet autenticado")

        update_data = {'content': 'Teste tweet editado autenticado'}

        url = reverse('update_tweet', args=[tweet.id])
        response = self.authenticated_client.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, 200)
        tweet.refresh_from_db()
        self.assertEqual(tweet.content, 'Teste tweet editado autenticado')

    
    #teste para editar tweet sem autorização
    def test_update_tweet_unauthorized(self):

        owner = User.objects.create_user(username="dono", password="1234")

        tweet = Tweet.objects.create(user=owner, content="Tweet original")

        impostor = User.objects.create_user(username="impostor", password="1234")
        client_impostor = APIClient()
        client_impostor.force_authenticate(user = impostor)

        update_data = {'content': 'Teste tweet editado sem autorização'}

        url = reverse('update_tweet', args=[tweet.id])
        response = client_impostor.patch(url, update_data, format='json')

        self.assertEqual(response.status_code, 403)
        tweet.refresh_from_db()
        self.assertEqual(tweet.content, "Tweet original")

    
    #teste para deletar tweet autorizado
    def test_delete_tweet_authenticated(self):

        tweet = Tweet.objects.create(user=self.authenticated_client, content="tweet para deleção")

        url = reverse('delete_tweet', args=[tweet.id])
        response = self.authenticated_client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Tweet.objects.count(), 0)

    
    #teste para deletar tweet sem autorização
    def test_delete_tweet_unauthorized(self):

        
        owner = User.objects.create_user(username="dono", password="1234")

        tweet = Tweet.objects.create(user=owner, content="Tweet original")

        impostor = User.objects.create_user(username="impostor", password="1234")
        client_impostor = APIClient()
        client_impostor.force_authenticate(user = impostor)


        url = reverse('delete_tweet', args=[tweet.id])
        response = client_impostor.delete(url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tweet.objects.count(), 1)


    #teste para curtir ou descurtir tweet autorizado
    def test_like_dislike_function_authenticated(self):

        tweet = Tweet.object.create(user=self.authenticated_client, content="Tweet para teste de curtida")

        url = reverse('like-dislike', args=[tweet.id])

        #response para like
        response_like = self.authenticated_client.post(url)
        self.assertEqual(response_like.status_code, 204)
        self.assertTrue(tweet.likes.filter(id=self.authenticated_client.id).exists())

        #response para dislike
        response_dislike = self.authenticated_client.post(url)
        self.assertEqual(response_dislike.status_code, 204)
        self.assertTrue(tweet.likes.filter(id=self.authenticated_client.id).exists())

    
    #teste para curtir ou descurtir tweet sem autorização
    def test_like_dislike_function_unauthorized(self):

        tweet = Tweet.object.create(user=self.authenticated_client, content="Tweet para teste de curtida sem autorização")

        url = reverse('like-dislike', args=[tweet.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 401)

    
    #teste para pesquisa aunteticado
    def test_search_function_authenticated(self):

        Tweet.object.create(user=self.authenticated_client, content="Tweet para teste de pesquisa autorizado")
        Tweet.object.create(user=self.authenticated_client, content="Tweet sem a palabra desejada")

        response = self.authenticated_client.get('/tweets/search/?q=pesquisa')

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn('pesquisa', response.data[0]['content'])

    
    #teste para pesquisa sem autorização
    def test_search_function_unauthorized(self):

        Tweet.object.create(user=self.authenticated_client, content="Tweet para teste de pesquisa autorizado")
        Tweet.object.create(user=self.authenticated_client, content="Tweet sem a palabra desejada")

        response = self.client.get('/tweets/search/?q=pesquisa')

        self.assertEqual(response.status_code, 401)
