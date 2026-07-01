from django.contrib import admin
from .models import Post, Like, Hashtag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('author', 'content_preview', 'like_count', 'created_at')
    list_filter   = ('created_at',)
    search_fields = ('content', 'author__email')
    readonly_fields = ('created_at', 'updated_at')

    def content_preview(self, obj):
        return obj.content[:60]
    content_preview.short_description = 'Content'

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')