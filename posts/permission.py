from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    커스텀 권한 클래스:
    - 권한 없는 사용자: 목록과 상세보기만 가능
    - MEMBER: 작성, 자신이 작성한 것에 대해 수정/삭제 가능
    - ADMIN: 모든 CRUD 가능
    """

    def has_permission(self, request, view):
        # 목록 조회와 상세 조회는 모든 사용자에게 허용
        if view.action in ['list', 'retrieve']:
            return True

        # 생성은 인증된 사용자만 가능
        if view.action == 'create':
            return request.user.is_authenticated

        # 수정/삭제는 인증된 사용자만 가능 (객체 레벨에서 추가 확인)
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 사용자에게 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 인증되지 않은 사용자는 수정/삭제 불가
        if not request.user.is_authenticated:
            return False

        # ADMIN은 모든 권한 허용
        if request.user.role == 'ADMIN':
            return True

        # MEMBER는 자신이 작성한 것만 수정/삭제 가능
        if request.user.role == 'MEMBER':
            return obj.author == request.user

        return False