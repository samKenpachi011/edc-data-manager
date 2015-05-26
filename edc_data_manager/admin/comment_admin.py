from django.contrib import admin

from ..models import Comment

from .base_admin import BaseAdmin


class CommentAdmin(BaseAdmin):
        pass
admin.site.register(Comment, CommentAdmin)
