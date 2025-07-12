from rest_framework import serializers
from django.contrib.auth import authenticate # 사용자 인증을 위한 함수
from django.contrib.auth.password_validation import validate_password # 비밀번호 유효성 검사를 위한 함수
from .models import User

# 사용자 정보 조회를 위한 Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'created_at') # 포함할 필드
        read_only_fields = ('id', 'created_at') # 읽기 전용 필드

# 회원가입을 위한 Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password]) # 비밀번호 필드 (쓰기 전용, 유효성 검사 적용)
    password_confirm = serializers.CharField(write_only=True) # 비밀번호 확인 필드 (쓰기 전용)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'role') # 회원가입 시 받을 필드

    def validate(self, attrs):
        # 비밀번호와 비밀번호 확인이 일치하는지 검증
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return attrs

    def create(self, validated_data):
        # 비밀번호 확인 필드는 저장하지 않으므로 제거
        validated_data.pop('password_confirm')
        # User 모델의 create_user 메서드를 사용하여 사용자 생성 (비밀번호가 해싱됨)
        user = User.objects.create_user(**validated_data)
        return user

# 로그인을 위한 Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField() # 사용자명 입력 필드
    password = serializers.CharField() # 비밀번호 입력 필드

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # authenticate 함수를 사용하여 사용자 인증 시도
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('로그인 정보가 올바르지 않습니다.') # 인증 실패 시 오류
            if not user.is_active:
                raise serializers.ValidationError('계정이 비활성화되었습니다.') # 비활성화된 계정인 경우 오류
            attrs['user'] = user # 유효성 검사를 통과한 사용자 객체를 attrs에 추가
        else:
            raise serializers.ValidationError('사용자명과 비밀번호를 입력해주세요.') # 사용자명 또는 비밀번호가 없는 경우 오류
        return attrs