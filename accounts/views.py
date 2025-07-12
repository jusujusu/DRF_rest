# accounts/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes  # 함수 기반 뷰를 위한 데코레이터
from rest_framework.permissions import AllowAny  # 모든 사용자에게 접근을 허용하는 권한 클래스
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken  # JWT 토큰 생성을 위한 RefreshToken 임포트

from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer


@api_view(['POST']) # POST 요청만 허용하는 API 뷰
@permission_classes([AllowAny]) # 모든 사용자가 접근 가능 (회원가입은 인증 필요 없음)
def register(request):
    """회원가입 API"""
    serializer = UserRegistrationSerializer(data=request.data) # 요청 데이터로 Serializer 초기화
    if serializer.is_valid(): # 데이터 유효성 검사
        user = serializer.save() # 사용자 저장
        refresh = RefreshToken.for_user(user) # 새로 생성된 사용자를 위한 리프레시 토큰 발급
        return Response({
            'message': '회원가입이 완료되었습니다.',
            'user': UserSerializer(user).data, # 사용자 정보 직렬화
            'refresh': str(refresh),          # 리프레시 토큰
            'access': str(refresh.access_token), # 액세스 토큰
        }, status=status.HTTP_201_CREATED) # 201 Created 응답
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 유효성 검사 실패 시 오류 응답

@api_view(['POST']) # POST 요청만 허용하는 API 뷰
@permission_classes([AllowAny]) # 모든 사용자가 접근 가능 (로그인은 인증 필요 없음)
def login(request):
    """로그인 API"""
    serializer = LoginSerializer(data=request.data) # 요청 데이터로 Serializer 초기화
    if serializer.is_valid(): # 데이터 유효성 검사
        user = serializer.validated_data['user'] # 유효성 검사를 통과한 사용자 객체 가져오기
        refresh = RefreshToken.for_user(user) # 사용자에게 리프레시 토큰 발급
        return Response({
            'message': '로그인이 완료되었습니다.',
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }) # 성공 응답
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 유효성 검사 실패 시 오류 응답

@api_view(['GET']) # GET 요청만 허용하는 API 뷰
# 권한 클래스를 명시하지 않으면 settings.py의 DEFAULT_PERMISSION_CLASSES(IsAuthenticated)가 적용됨.
# 즉, 이 뷰는 인증된 사용자만 접근 가능.
def profile(request):
    """내 프로필 조회 API"""
    serializer = UserSerializer(request.user) # 현재 로그인된 사용자 정보 직렬화
    return Response(serializer.data) # 사용자 데이터 반환