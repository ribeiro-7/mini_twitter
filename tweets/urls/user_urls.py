from django.urls import path
from tweets.views.user_views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', registerUser, name='register'),
    path('profile/', getUserProfile, name='user_profile'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logoutUser, name='user_logout'),
    path('delete/', deleteUser, name='delete_user'),
]
