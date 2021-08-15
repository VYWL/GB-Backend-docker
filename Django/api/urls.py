from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import BoardView, CommentView, ArticleView, LikeLogView

article_list = ArticleView.as_view({
    'post': 'create',
    'get': 'list',
})

article_detail = ArticleView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

board_list = BoardView.as_view({
    'post': 'create',
    'get': 'list',
})

board_detail = BoardView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

comment_list = CommentView.as_view({
    'post': 'create',
    'get': 'list',
})

comment_list_detail = CommentView.as_view({
    'get': 'retrieve',
    'delete' : 'destroy'
})

like_list = LikeLogView.as_view({
    'post': 'create',
    'get' : 'list',
})


urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('article/', article_list, name='article_list'),
    path('article/<int:pk>/', article_detail, name='article_detail'),
    path('board/', board_list, name='board_list'),
    path('board/<int:pk>', board_detail, name='board_detail'),
    path('comment/', comment_list, name='comment_list'),
    path('comment/<int:pk>/', comment_list_detail, name='comment_list_detail'),
    path('like/', like_list, name='like_list'),
])