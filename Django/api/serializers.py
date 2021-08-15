from rest_framework import serializers
from .models import Board, Comment, LikeLog, Article

###
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeLog
        fields = '__all__'