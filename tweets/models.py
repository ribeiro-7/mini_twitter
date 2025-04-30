from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.content} - Tweet de {self.user} - Criado em {self.created_at}"