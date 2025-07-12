
"""
boot에서 DTO의 역할
기능별로 필요한 데이터 값을 가져올 시리얼라이저를 만들어서 사용 가능
"""


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'role')


# 포스트 목록용 serializer - 댓글 수 포함
class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'comments_count', 'created_at', 'updated_at')

    # 댓글 수 생성
    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'post', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    # 로그인 한 사용자의 정보를 가져옴
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'comments', 'comments_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def get_comments_count(self, obj):
        return obj.comments.count()

    # 로그인 한 사용자의 정보를 가져옴
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

