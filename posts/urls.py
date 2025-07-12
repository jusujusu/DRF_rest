from django.urls import path, include
from rest_framework.routers import DefaultRouter # 자동 URL 라우팅을 위한 DefaultRouter
from .views import PostViewSet, CommentViewSet

# 라우터 인스턴스를 생성
router = DefaultRouter()
# PostViewSet을 'posts' 접두사로 등록 /api/posts/, /api/posts/{id}/와 같은 URL이 생성
router.register(r'posts', PostViewSet)
# CommentViewSet을 'comments' 접두사로 등록 /api/comments/, /api/comments/{id}/와 같은 URL이 생성
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)), # 라우터에 의해 생성된 모든 URL을 포함
]

