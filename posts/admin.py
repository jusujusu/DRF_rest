from django.contrib import admin
from .models import Post, Comment


# 기존에 사용하던 방식
# admin.site.register(Post)
# admin.site.register(Comment)


# 데코레이터 사용 방식
# 관리자 페이지에서 보여줄 테이블
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('content',)
    readonly_fields = ('created_at', 'updated_at')

