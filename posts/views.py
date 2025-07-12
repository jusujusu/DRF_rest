from rest_framework import viewsets, status
from rest_framework.decorators import action # 커스텀 액션을 위한 데코레이터
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Post, Comment
from .permission import IsOwnerOrAdminOrReadOnly
from .serializers import PostSerializer, PostListSerializer, CommentSerializer


"""
comment를 가져오는 방법은 post에 post 조회 메서드, comment 뷰셋을 이용한 두 가지 방법이 적용 중
두 방법은 가져오는 결과는 같지만 url 생성의 차이가 있음

1. post 뷰셋에서 comments get 메서드는 
    GET /posts/{post_id}/comments/ 
2. comment 뷰셋에서는    
    GET /comments/?post_id=12  

어느 model을 기준으로 삼을지에 대해 url 주소가 달라지게 됨
post를 중심으로 할거면 post 뷰셋에 관련된 comment의 정보를 가져오는 메서드 생성

"""



# Post 모델을 위한 ViewSet으로, 모든 CRUD 작업을 자동으로 제공
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all() # ViewSet을 위한 쿼리셋
    # IsOwnerOrAdminOrReadOnly: 소유자나 관리자만 수정/삭제 가능하며, 그 외에는 읽기만 가능
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    # 액션에 따라 동적으로 Serializer를 선택
    def get_serializer_class(self):
        # action이 'list'일 때
        if self.action == 'list':
            return PostListSerializer # 목록 보기에는 간략한 Serializer 사용
        return PostSerializer         # 다른 액션(조회, 생성, 업데이트)에는 상세 Serializer 사용

    # 특정 포스트의 댓글 조회
    # url : /api/posts/{post_id}/comments/
    @action(detail=True, methods=['get'])   # @action을 사용해서 내부적으로 라우팅 경로 생성
    def comments(self, request, pk=None):   # GET /posts/<pk>/comments/ 이런 url이 생성됨
        post = self.get_object() # 특정 Post 인스턴스 가져오기
        comments = post.comments.all() # 이 게시물과 관련된 모든 댓글 가져오기
        serializer = CommentSerializer(comments, many=True) # 댓글 직렬화
        return Response(serializer.data)

    # 특정 포스트에 댓글 작성
    # permission_classes=[IsAuthenticatedOrReadOnly]: 이 특정 액션에는 별도의 권한을 적용합니다.
    #   인증된 사용자만 댓글을 작성(POST)할 수 있으며, 인증되지 않은 사용자는 읽기만 가능
    # url : /api/posts/{post_id}/add_comment/
    @action(detail=True, methods=['post'] ,permission_classes=[IsAuthenticatedOrReadOnly])
    def add_comment(self, request, pk=None):
        post = self.get_object() # 특정 Post 인스턴스 가져오기
        # 클라이언트로부터 받은 요청 데이터(request.data)로 CommentSerializer를 초기화합니다.
        # context={'request': request}: Serializer의 create/update 메서드에서 request.user와 같은
        #   요청 컨텍스트에 접근할 수 있도록 현재 요청 객체를 전달합니다.
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(): # 들어오는 데이터 유효성 검사
            serializer.save(post=post) # 댓글 저장, 현재 게시물에 연결
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 성공 응답 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 유효성 검사 실패 시 오류 반환



# Comment 모델을 위한 ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # IsOwnerOrAdminOrReadOnly: 소유자나 관리자만 수정/삭제 가능하며, 그 외에는 읽기만 가능
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    # 쿼리 파라미터로 특정 포스트의 댓글 필터링
    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id') # 쿼리 파라미터에서 'post_id' 가져오기
        if post_id:
            queryset = queryset.filter(post_id=post_id) # post_id로 댓글 필터링
        return queryset