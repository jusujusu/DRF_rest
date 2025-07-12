# 기존 DRF 사용
# 포스트 CRUD
GET /api/posts/                    # 포스트 목록 조회
POST /api/posts/                   # 포스트 생성
{
    "title": "제목",
    "content": "내용",
    "author_username": "admin"
}

GET /api/posts/{id}/               # 포스트 상세 조회
PUT /api/posts/{id}/               # 포스트 수정
DELETE /api/posts/{id}/            # 포스트 삭제

# 댓글 CRUD (사용자 이름 기반)
GET /api/comments/                 # 모든 댓글 조회
GET /api/comments/?post_id={id}    # 특정 포스트의 댓글 조회
POST /api/comments/                # 댓글 생성
{
    "content": "댓글 내용",
    "author_username": "admin",
    "post_id": 1
}

GET /api/comments/{id}/            # 댓글 상세 조회
PUT /api/comments/{id}/            # 댓글 수정
DELETE /api/comments/{id}/         # 댓글 삭제

# 포스트별 댓글 관련 API
GET /api/posts/{id}/comments/      # 특정 포스트의 댓글 조회
POST /api/posts/{id}/add_comment/  # 특정 포스트에 댓글 작성
{
    "content": "댓글 내용",
    "author_username": "admin"
}


# DRF + JWT 사용 
1. 회원가입
POST /api/auth/register/
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "role": "MEMBER"
}

2. 로그인
POST /api/auth/login/
{
    "username": "testuser",
    "password": "testpass123"
}

3. 토큰 갱신
POST /api/auth/token/refresh/
{
    "refresh": "your-refresh-token"
}

4. 프로필 조회 (인증 필요)
GET /api/auth/profile/
Headers: Authorization: Bearer your-access-token

5. 포스트 API (권한 적용)
GET /api/posts/                    # 모든 사용자 접근 가능
GET /api/posts/{id}/               # 모든 사용자 접근 가능
POST /api/posts/                   # 인증된 사용자만 가능
Headers: Authorization: Bearer your-access-token
{
    "title": "제목",
    "content": "내용"
}

PUT /api/posts/{id}/               # 작성자 또는 ADMIN만 가능
Headers: Authorization: Bearer your-access-token
{
    "title": "수정된 제목",
    "content": "수정된 내용"
}

DELETE /api/posts/{id}/            # 작성자 또는 ADMIN만 가능
Headers: Authorization: Bearer your-access-token

6. 댓글 API (권한 적용)
GET /api/comments/                 # 모든 사용자 접근 가능
GET /api/comments/{id}/            # 모든 사용자 접근 가능
POST /api/comments/                # 인증된 사용자만 가능
Headers: Authorization: Bearer your-access-token
{
    "content": "댓글 내용",
    "post": 1
}

PUT /api/comments/{id}/            # 작성자 또는 ADMIN만 가능
Headers: Authorization: Bearer your-access-token
{
    "content": "수정된 댓글 내용"
}

DELETE /api/comments/{id}/         # 작성자 또는 ADMIN만 가능
Headers: Authorization: Bearer your-access-token

7. 포스트별 댓글 API
GET /api/posts/{id}/comments/      # 특정 포스트의 댓글 조회
POST /api/posts/{id}/add_comment/  # 특정 포스트에 댓글 작성
Headers: Authorization: Bearer your-access-token
{
    "content": "댓글 내용"
}
