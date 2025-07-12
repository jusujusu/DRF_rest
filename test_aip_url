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