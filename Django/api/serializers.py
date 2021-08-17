from rest_framework import serializers
from .models import Board, Comment, File, Image, LikeLog, Article

###
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class ArticleReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('boardid', 'articleid', 'title', 'content', 'timestamp', 'vote', 'unlike', 'commentcount', 'writer', 'isanony', 'filecount', 'imagecount', 'thumbnail')

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('articleid', 'commentid', 'content', 'timestamp', 'parentcid', 'vote', 'unlike', 'writer','isanony', 'isreply', 'isdel', 'isvisible')

class LikeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeLog
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        # fields = ('articleid', 'fid', 'uuid', 'filename', 'filesize', 'timestamp')

class FileReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('fid', 'uuid', 'filename', 'filesize', 'timestamp')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        # fields = ('articleid', 'fid', 'uuid', 'filename', 'filesize', 'timestamp')
        
class ImageReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('fid', 'uuid', 'filename', 'filesize', 'timestamp')
        