from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'created_at', 'slug']
    list_filter = ['author']
    search_fields = ['content', 'author__name__icontains']
    date_hierarchy = 'created_at'
    readonly_fields = ['id', 'created_at', 'slug']
    list_per_page = 15

class CommentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'content', 'post']
    list_filter = ['owner']
    search_fields = ['owner__name__icontains', 'content', 'post__content__icontains']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    list_per_page = 15

class NotificateAdmin(admin.ModelAdmin):
    list_display = ['receiver', 'sender', 'post', 'islem', 'created_at', 'isRead']
    list_filter = ['islem', 'isRead']
    search_fields = ['receiver__name__icontains', 'sender__name__icontains', 'post__content__icontains']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    list_per_page = 15

admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Notificate, NotificateAdmin)