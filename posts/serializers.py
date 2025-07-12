from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment


"""
boot에서 DTO의 역할 
기능별로 필요한 데이터 값을 가져올 시리얼라이저를 만들어서 사용 가능
"""


# User 모델 serializer
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        # 직렬화할 모델
        model = User
        # 직렬화에 포함할 필드
        fields = ('id', 'username')



# Class 모델 serializer,
class CommentSerializer(serializers.ModelSerializer):
    # 'author' 필드는 AuthorSerializer를 사용하여 직렬화 (읽기 전용).
    author = AuthorSerializer(read_only=True)
    # 'author_id'는 쓰기 전용 필드로, 작성자 ID를 사용하여 댓글을 생성/업데이트하는 데 사용
    author_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        # 직렬화에 포함할 필드.
        fields = ('id', 'content', 'author', 'author_id', 'created_at', 'updated_at')
        # 읽기 전용 필드 (클라이언트에서 설정할 수 없음).
        read_only_fields = ('id', 'created_at', 'updated_at')

    # author_id를 처리하기 위한 커스텀 생성 메서드
    def create(self, validated_data):
        # DRF는 뷰셋에 의해 validated_data에 'post' 필드가 있는 경우 이를 자동으로 처리
        return Comment.objects.create(**validated_data)


# Post 모델 serializer, 상세 보기(조회, 생성, 업데이트)에 사용
class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)      # 작성자를 위한 중첩 Serializer
    author_id = serializers.IntegerField(write_only=True) # 작성자 ID를 위한 쓰기 전용 필드
    comments = CommentSerializer(many=True, read_only=True) # 댓글을 위한 중첩 Serializer (게시물당 여러 댓글)
    comments_count = serializers.SerializerMethodField() # 댓글 수를 가져오기 위한 커스텀 필드

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'author_id', 'comments', 'comments_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    # 게시물의 댓글 수를 계산하는 메서드
    def get_comments_count(self, obj):
        return obj.comments.count()


    # author_id를 처리하기 위한 커스텀 생성 메서드
    def create(self, validated_data):
        return Post.objects.create(**validated_data)



# Post 모델의 Serializer, 목록 보기(간략한 정보)에 사용.
class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # 목록 보기를 위한 필드. 'content'는 제외
        fields = ('id', 'title', 'author', 'comments_count', 'created_at', 'updated_at')

    def get_comments_count(self, obj):
        return obj.comments.count()
