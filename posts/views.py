from rest_framework import viewsets, status
from rest_framework.decorators import action # 커스텀 액션을 위한 데코레이터
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, PostListSerializer, CommentSerializer


# Post 모델을 위한 ViewSet으로, 모든 CRUD 작업을 자동으로 제공
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all() # ViewSet을 위한 쿼리셋

    # 액션에 따라 동적으로 Serializer를 선택
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer # 목록 보기에는 간략한 Serializer 사용
        return PostSerializer         # 다른 액션(조회, 생성, 업데이트)에는 상세 Serializer 사용

    # 특정 포스트의 댓글 조회
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object() # 특정 Post 인스턴스 가져오기
        comments = post.comments.all() # 이 게시물과 관련된 모든 댓글 가져오기
        serializer = CommentSerializer(comments, many=True) # 댓글 직렬화
        return Response(serializer.data)

    # 특정 포스트에 댓글 작성
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        post = self.get_object() # 특정 Post 인스턴스 가져오기
        serializer = CommentSerializer(data=request.data) # 요청 데이터로 Serializer 초기화
        if serializer.is_valid(): # 들어오는 데이터 유효성 검사
            serializer.save(post=post) # 댓글 저장, 현재 게시물에 연결
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 성공 응답 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 유효성 검사 실패 시 오류 반환



# Comment 모델을 위한 ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # 쿼리 파라미터로 특정 포스트의 댓글 필터링
    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id') # 쿼리 파라미터에서 'post_id' 가져오기
        if post_id:
            queryset = queryset.filter(post_id=post_id) # post_id로 댓글 필터링
        return queryset