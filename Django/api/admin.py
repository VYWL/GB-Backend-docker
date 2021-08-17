from django.contrib import admin
from .models import Board, Comment, Article, File, Image, LikeLog

admin.site.register(Article)
admin.site.register(Board)
admin.site.register(Comment)
admin.site.register(File)
admin.site.register(Image)
admin.site.register(LikeLog)