from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    커스텀 권한 클래스:
    - 권한 없는 사용자: 목록과 상세보기만 가능 (읽기 전용)
    - MEMBER: 생성 가능, 자신이 작성한 것에 대해 수정/삭제 가능
    - ADMIN: 모든 CRUD (생성, 조회, 수정, 삭제) 가능
    """

    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS 요청은 항상 허용 (읽기 작업)
        if request.method in permissions.SAFE_METHODS:
            return True

        # 목록 조회 (list)와 상세 조회 (retrieve)는 모든 사용자에게 허용
        # 이 부분은 SAFE_METHODS와 중복되지만, 명시적으로 뷰 액션을 지정하는 것도 가능
        if view.action in ['list', 'retrieve']:
            return True

        # 생성 (create)는 인증된 사용자만 가능
        if view.action == 'create':
            return request.user.is_authenticated

        # 그 외의 작업 (수정/삭제 등)은 인증된 사용자만 가능 (객체 레벨에서 추가 확인)
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 사용자에게 허용 (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # 인증되지 않은 사용자는 수정/삭제 불가
        if not request.user.is_authenticated:
            return False

        # ADMIN 역할의 사용자는 모든 권한 허용 (객체에 대한 모든 작업 가능)
        if request.user.role == 'ADMIN':
            return True

        # MEMBER 역할의 사용자는 자신이 작성한 객체만 수정/삭제 가능
        if request.user.role == 'MEMBER':
            return obj.author == request.user  # 현재 객체의 작성자가 요청한 사용자인지 확인

        return False  # 위에 해당하지 않는 경우 (예: 정의되지 않은 역할 등)에는 접근 불허