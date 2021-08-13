from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostView, BoardView, CommentView

#####
from .views import article_list
######


#article_list = article_list.as_view({
#    'post': 'create',
#    'get': 'list',
#})


post_list = PostView.as_view({
    'post': 'create',
    'get': 'list'
})

post_detail = PostView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


#article_detail = ArticleView.as_view({
#    'get': 'retrieve',
#    'put': 'update',
#    'patch': 'partial_update',
#    'delete': 'destroy'
#})

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

comment_detail = CommentView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('posts/', post_list, name='post_list'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('article/', article_list, name='article_list'),
  #  path('article/<int:pk>/', article_detail, name='article_detail'),
    path('board/', board_list, name='board_list'),
    path('board/<int:pk>/', board_detail, name='board_detail'),
    path('comment/', comment_list, name='comment_list'),
    path('comment/<int:pk>/', comment_detail, name='comment_detail'),
])