from django.contrib.auth.models import AbstractUser
from django.db import models


# 커스텀 User 모델 정의
class User(AbstractUser):
    # 사용자 역할을 정의하는 선택지
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),  # 관리자 역할
        ('MEMBER', 'Member'),  # 일반 멤버 역할
    ]

    # 역할 필드: 최대 길이 10, ROLE_CHOICES 중 하나를 선택, 기본값은 'MEMBER'
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시 자동으로 현재 시간 기록
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 시 자동으로 현재 시간 기록

    def __str__(self):
        # 객체를 문자열로 표현할 때 사용 (예: 관리자 페이지 등)
        return f"{self.username} ({self.role})"