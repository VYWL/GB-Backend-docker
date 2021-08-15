from django.contrib import admin
from .models import Board, Comment, Article, LikeLog

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Board)
admin.site.register(LikeLog)



