from django.shortcuts import render
##
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
##
# Create your views here.
from rest_framework import viewsets
from .serializers import BoardSerializer, CommentSerializer, PostSerializer, ArticleSerializer
from .models import Board, Comment, Post, Article
from rest_framework import permissions

###
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# @api_view(['GET', 'POST'])
# def article_list(request):
#     """
#     List all code articles, or create a new Article.
#     """
#     if request.method == 'GET':
#       #  articles = Article.objects.all()
#         queryset = Article.objects.raw('SELECT * FROM Article')
#         serializer = ArticleSerializer(queryset, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.raw('SELECT * FROM Article')
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save()

#    def create(requ)


class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.raw('SELECT * FROM Board')
    serializer_class = BoardSerializer

    def perform_create(self, serializer):
        serializer.save()
        # return 


        
class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.raw('SELECT * FROM Comment')
    serializer_class = CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save()