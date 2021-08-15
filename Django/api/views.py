from django.db.models import query
from django.shortcuts import render, get_object_or_404
##
from django.http import HttpResponse, JsonResponse
##
# Create your views here.
from rest_framework import viewsets
from .serializers import BoardSerializer, CommentSerializer,  ArticleSerializer, LikeLogSerializer
from .models import Board, Comment, Article, LikeLog

###
from rest_framework.response import Response

class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.raw('SELECT * FROM Article WHERE isDel=0')
    serializer_class = ArticleSerializer

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, pk):
        article = Article.objects.get(articleid=pk)

        # password_valid
        isCorrect = article.password == request.data['password']

        msg = "failed"

        if isCorrect: 
            article.isdel = True
            article.save()
            msg = "success"
        
        return Response({'msg' : msg})

class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.raw('SELECT * FROM Board WHERE isDel=0')
    serializer_class = BoardSerializer
    
    def perform_create(self, serializer):
        serializer.save()
 
class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.raw('SELECT * FROM Comment WHERE isDel=0')
    serializer_class = CommentSerializer

    def retrieve(self, request, pk):
        qusrystring = 'SELECT * FROM Comment WHERE articleID={} AND isDel=0 \
                       ORDER BY parentCID, timestamp ASC'.format(pk)
        queryset = Comment.objects.raw(qusrystring)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        comment = Comment.objects.get(commentid=pk)

        # password_valid
        isCorrect = comment.password == request.data['password']

        msg = "failed"

        if isCorrect: 
            comment.isdel = True
            comment.save()
            msg = "success"
        
        return Response({'msg' : msg})
    
    def perform_create(self, serializer):
        serializer.save()

class LikeLogView(viewsets.ModelViewSet):
    queryset = LikeLog.objects.raw('SELECT * FROM LikeLog')
    serializer_class = LikeLogSerializer
    
    def create(self, request):
        serializer=LikeLogSerializer(data=request.data)
        isUnlike = 'isunlike' in request.data
        isUnlikeValue = 1 if isUnlike else 0
        isArticle = 'articleid' in request.data

        articleQuery = "SELECT * FROM LikeLog WHERE articleID={} AND isunlike={}".format(request.data["articleid"], isUnlikeValue)
        commentQuery = "SELECT * FROM LikeLog WHERE commentID={} AND isunlike={}".format(request.data["commentid"], isUnlikeValue)

        queryString =  articleQuery if isArticle else commentQuery
        LikelogList = LikeLog.objects.raw(queryString)

        if(len(list(LikelogList)) == 0):            
            if isArticle :
                article = Article.objects.get(articleid=request.data['articleid'])
                if isUnlike :
                    article.unlike = article.unlike + 1
                else:
                    article.vote = article.vote + 1

                article.save()
            else :       
                comment = Comment.objects.get(commentid=request.data['commentid'])
                if isUnlike :
                    comment.unlike = comment.unlike + 1
                else:
                    comment.vote = comment.vote + 1

                comment.save()

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({'msg' : "success"})
        else:
            return Response({'msg' : "fail"})
            
    def perform_create(self, serializer):
        serializer.save()