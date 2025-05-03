from django.test import TestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient


class TweetsModelTest(TestCase):

    def authenticated_user(self):
        self.user = User.objects.create_user(username="user_test", password="1234")
        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=self.user)


    #teste para criar um tweet com conteudo e imagem
    def test_create_tweet_complete(self):

        self.authenticated_user()

        image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/jpeg'
        )

        tweet = Tweet.objects.create(user=self.user, content='Conteúdo do tweet', image=image)
        self.assertEqual(tweet.content, 'Conteúdo do tweet')
        self.assertEqual(tweet.user.username, 'user_test')
        self.assertTrue(tweet.image.name.endswith('.jpg'))


    #teste para criar tweet apenas com conteúdo
    def test_create_tweet_with_only_content(self):

        self.authenticated_user()
        
        tweet = Tweet.objects.create(user=self.user, content='Conteúdo do tweet')
        self.assertEqual(tweet.content, 'Conteúdo do tweet')
        self.assertEqual(tweet.user.username, 'user_test')
        self.assertFalse(tweet.image.name)

    
    #teste para criar tweet apenas com imagem
    def test_tweet_with_only_image(self):

        self.authenticated_user()

        image = SimpleUploadedFile(
            name='test.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/jpeg'
        )

        tweet = Tweet.objects.create(user=self.user, image=image)
        self.assertFalse(tweet.content)
        self.assertEqual(tweet.user.username, 'user_test')
        self.assertTrue(tweet.image.name.endswith('.jpg'))

    #teste para relação de like
    def test_likes_relationship(self):

        self.authenticated_user()

        another_user = User.objects.create_user(username='user2', password='1234')
        tweet = Tweet.objects.create(user=self.user, content='Teste de like')
        tweet.likes.add(another_user)
        self.assertEqual(tweet.likes.count(), 1)
        self.assertTrue(tweet.likes.filter(username='user2').exists())


    #teste para edição de tweet
    def test_update_tweet(self):

        self.authenticated_user()

        tweet = Tweet.objects.create(user=self.user, content="Contéudo para editar")

        update_data = {'content': 'Conteúdo editado'}

        url = reverse('update_tweet', args=[tweet.id])

        self.authenticated_client.patch(url, update_data, format='json')

        tweet.refresh_from_db()

        self.assertEqual(tweet.content, 'Conteúdo editado')

    
    #teste para deleção de tweet
    def test_delete_tweet(self):

        self.authenticated_user()

        tweet = Tweet.objects.create(user=self.user, content="Contéudo para apagar")

        url = reverse('delete_tweet', args=[tweet.id])

        self.authenticated_client.delete(url)

        self.assertEqual(Tweet.objects.count(), 0)