from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile



class ProfileModelTest(TestCase):

    def setUp(self):

        self.follower = User.objects.create_user(username='seguidor', password='1234')
        self.target = User.objects.create_user(username='alvo', password='1234')
        self.follower_profile = Profile.objects.get(user=self.follower)
        self.target_profile = Profile.objects.get(user=self.target)


    #teste para relação de follow e unfollow do modelo profile
    def test_follow_relashionsip(self):
        
        self.target_profile.followers.add(self.follower)
        self.assertIn(self.follower, self.target_profile.followers.all())

        self.target_profile.followers.remove(self.follower)
        self.assertNotIn(self.follower, self.target_profile.followers.all())