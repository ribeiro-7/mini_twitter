from django.urls import path
from tweets.views.user_views import *

urlpatterns = [
    path('register/', registerUser, name='register'),
    path('profile/', getUserProfile, name='user_profile'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('delete/<str:pk>', deleteUser, name='delete_user'),
]
