
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
        fields = ('id', 'username')


class PostListSerializer(serializers.ModelSerializer):
    """포스트 목록용 간단한 serializer"""
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_username = serializers.CharField(write_only=True)  # 사용자 이름 입력받기
    post_id = serializers.IntegerField(write_only=True)  # post_id 필드 추가
    post = PostListSerializer(read_only=True)  # 읽기 전용 post 정보

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'author_username', 'post', 'post_id', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        # post_id를 post로 변환
        post_id = validated_data.pop('post_id')
        author_username = validated_data.pop('author_username')

        try:
            post = Post.objects.get(id=post_id)
            author = User.objects.get(username=author_username)
        except Post.DoesNotExist:
            raise serializers.ValidationError("해당 포스트가 존재하지 않습니다.")
        except User.DoesNotExist:
            raise serializers.ValidationError(f"사용자 '{author_username}'이 존재하지 않습니다.")

        return Comment.objects.create(
            post=post,
            author=author,
            **validated_data
        )


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_username = serializers.CharField(write_only=True)  # 사용자 이름 입력받기
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'author_username', 'comments', 'comments_count', 'created_at',
                  'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        author_username = validated_data.pop('author_username')
        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"사용자 '{author_username}'이 존재하지 않습니다.")

        return Post.objects.create(author=author, **validated_data)


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'comments_count', 'created_at', 'updated_at')

    def get_comments_count(self, obj):
        return obj.comments.count()