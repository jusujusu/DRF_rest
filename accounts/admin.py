from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # 기본 UserAdmin을 확장하기 위해 임포트
from .models import User

@admin.register(User) # Django 관리자 페이지에 User 모델을 등록
class CustomUserAdmin(UserAdmin):
    # 관리자 목록 페이지에 표시할 필드
    list_display = ('username', 'email', 'role', 'is_active', 'created_at')
    # 관리자 목록 페이지에 필터링 옵션 추가
    list_filter = ('role', 'is_active', 'created_at')
    # 기존 UserAdmin의 fieldsets에 '추가 정보' 섹션과 'role' 필드 추가 (사용자 정보 수정 페이지)
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('role',)}),
    )
    # 기존 UserAdmin의 add_fieldsets에 '추가 정보' 섹션과 'role' 필드 추가 (새 사용자 추가 페이지)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('추가 정보', {'fields': ('role',)}),
    )