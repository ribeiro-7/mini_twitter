from django.urls import path
from .views import followRelation

urlpatterns = [
    path('follow/<str:username>', followRelation, name='follow-relation'),
]