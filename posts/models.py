from django.conf import settings
from django.contrib.auth.models import User # Django의 내장 User 모델
from django.db import models


# 게시글
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    # author는 DRF 기존 User 모델로 연동
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 최신순으로 정렬
    class Meta:
        ordering = ['-created_at']

    # 가져오면 제목으로 표시
    def __str__(self):
        return self.title


# 댓글
class Comment(models.Model):
    # Post 모델에 대한 ForeignKey. 댓글을 특정 게시물과 연결
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # author는 DRF 기존 User 모델로 연동
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 최신순으로 정렬
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} - {self.post.title}'