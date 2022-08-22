from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import RegisterAPIView, activate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginView.as_view()),
    path('activation/', views.ActivationView.as_view()),
    path('users/', views.UserListAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('activate/<str:activation_code>/', activate),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]