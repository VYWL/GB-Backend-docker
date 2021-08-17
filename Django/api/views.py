from django.core.files.storage import FileSystemStorage
from django.db.models import query
from django.http.response import FileResponse
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.views.generic.detail import SingleObjectMixin
##
from django.http import HttpResponse, JsonResponse
##
# Create your views here.
import json, copy
from rest_framework import viewsets, status
from .serializers import ArticleReturnSerializer, BoardSerializer, CommentReturnSerializer, CommentSerializer,  ArticleSerializer, FileReturnSerializer, FileSerializer, ImageReturnSerializer, ImageSerializer, LikeLogSerializer
from .models import Board, Comment, Article, File, Image, LikeLog

###
from rest_framework.response import Response

class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.raw('SELECT * FROM Article WHERE isDel=0')
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"msg" : "success", "articleid": serializer.data["articleid"]}, status=status.HTTP_201_CREATED, headers=headers)


    def list(self, request):
        queryset = Article.objects.raw('SELECT * FROM Article WHERE isDel=0 \
                                        ORDER BY timestamp DESC')
        serializer = ArticleReturnSerializer(queryset, many=True)
        return Response(serializer.data)


    def update(self, request, pk):
        article = Article.objects.get(articleid=pk)
        data = request.data

        isValid = article.password == data["password"]

        msg = "fail"
        
        if isValid :
            article.title = data.get('title', article.title)
            article.content = data.get('content', article.content)
            article.isdel = data.get('isdel', article.isdel)

            if(article.isedit == False):
                article.isedit = True

            article.save()
            msg = "success"
        
        return Response({"msg" : msg})
        
    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleReturnSerializer(article)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, pk):
        article = Article.objects.get(articleid=pk)

        # password_valid
        isValid = article.password == request.data['password']

        msg = "fail"

        if isValid : 
            article.isdel = True
            article.save()

            deadComment = Comment.objects.filter(articleid=pk)
            deadComment.update(isdel=True)

            msg = "success"
        
        return Response({'msg' : msg})

class BoardView(viewsets.ModelViewSet):
    queryset = Board.objects.raw('SELECT * FROM Board')
    serializer_class = BoardSerializer
    
    def perform_create(self, serializer):
        serializer.save()
 
class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.raw('SELECT * FROM Comment WHERE isDel=0')
    serializer_class = CommentReturnSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        comment = Comment.objects.get(commentid=serializer.data["commentid"])
        
        if(comment.parentcid == 0): 
            comment.parentcid = comment.commentid
            comment.save()

        comment_result = serializers.serialize('json', [comment, ])
        comment_result_data = json.loads(comment_result)[0]["fields"]

        article = Article.objects.get(articleid=serializer.data["articleid"])
        article.commentcount = article.commentcount + 1
        article.save()

        headers = self.get_success_headers(serializer.data)
        return Response(comment_result_data, status=status.HTTP_201_CREATED, headers=headers)


    def retrieve(self, request, pk):
        qusrystring = 'SELECT * FROM Comment WHERE articleID={} AND isVisible=1 \
                       ORDER BY parentCID, timestamp ASC'.format(pk)
        queryset = Comment.objects.raw(qusrystring)
        serializer = CommentReturnSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        comment = Comment.objects.get(commentid=pk)

        # password_valid
        isCorrect = comment.password == request.data['password']

        msg = "fail"

        if isCorrect: 
            comment.isdel = True

            parentcid = int('{}'.format(comment.parentcid))
            childListLength = len(list(Comment.objects.raw('SELECT * FROM Comment WHERE parentCID={} AND isReply=1 AND isVisible=1'.format(parentcid))))

            if comment.isreply != True :
                if childListLength == 0 :
                    comment.isvisible = False
            else :
                if childListLength == 1 :
                    parentComment = Comment.objects.get(commentid=parentcid)
                    parentComment.isvisible = False
                    parentComment.save()
                comment.isvisible = False

            article = Article.objects.get(articleid=request.data["articleid"])
            article.commentcount = article.commentcount - 1
            article.save()
            
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

class FileView(viewsets.ModelViewSet):
    queryset = File.objects.raw('SELECT * FROM File')
    serializer_class = FileSerializer

    def create(self, request):
        receivedData = request.data

        if(receivedData["isnew"]):
            serializer = self.get_serializer(data=receivedData)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            articleid = request.data["articleid"]
            article = Article.objects.get(articleid=articleid)
            article.filecount = article.filecount + 1
            article.save()

            headers = self.get_success_headers(serializer.data)
            return Response({"msg" : "success"}, status=status.HTTP_201_CREATED, headers=headers)
        
        else:
            file = File.objects.get(fid=receivedData['fid'])
            file.isdel = receivedData['isdel']
            file.save()

            if(file.isdel):
                article = Article.objects.get(articleid=file.articleid)
                article.fileCount = article.fileCount - 1
                article.save()

            return Response({"msg" : "success"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        queryset = File.objects.raw('SELECT * FROM File WHERE isDel=0 AND articleID={} \
                                     ORDER BY timestamp ASC'.format(pk))
        serializer = FileReturnSerializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, uuid):
        file = File.objects.get(uuid=uuid)

        file_path = file.file.path
        # file_type = file.content_type
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename={file.get_filename()}'
        return response

    def update(self, request):
        receivedData = request.data

        file = File.objects.get(fid=receivedData['fid'])
        file.isdel = True if receivedData["isdel"] == 'true' else False
        file.save()
        msg = "data modificated"

        if(file.isdel):
            article = Article.objects.get(articleid=receivedData['articleid'])
            article.filecount = article.filecount - 1
            article.save()
            msg = "successfully applied"

        return Response({"msg" : "success", "detail": msg}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()


    
class ImageView(viewsets.ModelViewSet):
    queryset = Image.objects.raw('SELECT * FROM Image')
    serializer_class = ImageSerializer

    def create(self, request):
        receivedData = request.data

        serializer = self.get_serializer(data=receivedData)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        image = Image.objects.get(fid=serializer.data["fid"])
        image.isnew = False
        image.save()

        articleid = serializer.data["articleid"]
        article = Article.objects.get(articleid=articleid)

        if(article.imagecount == 0):
            article.thumbnail = '/api/upload/image/{}'.format(image.uuid)

        article.imagecount = article.imagecount + 1
        article.save()
        msg = "data generated"


        headers = self.get_success_headers(serializer.data)
        return Response({"msg" : "success", "detail": msg}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request):
        receivedData = request.data

        file = Image.objects.get(fid=receivedData['fid'])
        file.isdel = True if receivedData["isdel"] == 'true' else False
        file.save()
        msg = "data modificated"

        if(file.isdel):
            article = Article.objects.get(articleid=receivedData['articleid'])
            article.imagecount = article.imagecount - 1

            imageQS = Image.objects.filter(articleid=receivedData['articleid']) & Image.objects.filter(isdel=False)
            image = imageQS.order_by('timestamp')[0]

            article.thumbnail = '/api/upload/image/{}'.format(image.uuid)
            article.save()
            msg = "successfully applied"

        return Response({"msg" : "success", "detail": msg}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        queryset = Image.objects.raw('SELECT * FROM Image WHERE isDel=0 AND articleID={} \
                                      ORDER BY timestamp ASC'.format(pk))
        serializer = ImageReturnSerializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, uuid):
        image = Image.objects.get(uuid=uuid)

        file_path = image.file.path
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename={image.get_filename()}'
        return response
        
    def perform_create(self, serializer):
        serializer.save()