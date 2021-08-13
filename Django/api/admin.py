from django.contrib import admin
from .models import Board, Comment, Post, Article

admin.site.register(Post)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Board)



