from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_when = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

#cria o perfil automaticamente, assim que um usuario é criado
@receiver(post_save, sender=User)
def user_did_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)