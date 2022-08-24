from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import activate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('users/', views.UserListAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),
    path('activate/<str:activation_code>/', activate),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]