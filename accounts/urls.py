# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView # JWT 토큰 갱신 뷰
from . import views # 현재 앱의 views.py 임포트

urlpatterns = [
    path('register/', views.register, name='register'), # 회원가입 URL
    path('login/', views.login, name='login'),         # 로그인 URL
    path('profile/', views.profile, name='profile'),   # 프로필 조회 URL
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # JWT 토큰 갱신 URL
]