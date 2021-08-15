from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.contrib.auth.hashers import make_password


class Article(models.Model):
    boardid = models.ForeignKey('Board', models.DO_NOTHING, db_column='boardID')  # Field name made lowercase.
    articleid = models.AutoField(db_column='articleID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(db_column='timeStamp', null=True)  # Field name made lowercase.
    vote = models.IntegerField(default=0)
    unlike = models.IntegerField(default=0)
    writer = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=32, default="")
    isedit = models.BooleanField(db_column='isEdit', default=False)  # Field name made lowercase.
    isanony = models.BooleanField(db_column='isAnony', default=True)  # Field name made lowercase.
    isdel = models.BooleanField(db_column='isDel', default=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Article'
    
    def __str__(self):
        return '[articleID, title] : {}, {}'.format(self.articleid, self.title)


class Board(models.Model):
    boardname = models.CharField(db_column='boardName', max_length=20)  # Field name made lowercase.
    boardid = models.AutoField(db_column='boardID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Board'

    def __str__(self):
        return '[{}] {}'.format(self.boardid, self.boardname)


class Comment(models.Model):
    articleid = models.ForeignKey('Article', models.DO_NOTHING, db_column='articleID')  # Field name made lowercase.
    commentid = models.AutoField(db_column='commentID', primary_key=True)  # Field name made lowercase.
    content = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(db_column='timeStamp', null=True)  # Field name made lowercase.
    writer = models.CharField(max_length=20, blank=True, null=True)
    parentcid = models.IntegerField(db_column='parentCID', default=0)  # Field name made lowercase.
    password = models.CharField(max_length=32, default="")
    vote = models.IntegerField(default=0)
    isdel = models.BooleanField(db_column='isDel', default=False)  # Field name made lowercase.
    isanony = models.BooleanField(db_column='isAnony', default=True)  # Field name made lowercase.
    isreply = models.BooleanField(db_column='isReply', default=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comment'

        
class LikeLog(models.Model):
    articleid = models.ForeignKey('Article', models.DO_NOTHING, db_column='articleID', blank=True, null=True)  # Field name made lowercase.
    commentid = models.ForeignKey('Comment', models.DO_NOTHING, db_column='commentID', blank=True, null=True)  # Field name made lowercase.
    likeid = models.AutoField(db_column='likeID', primary_key=True)
    isunlike = models.BooleanField(db_column='isUnlike', default=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LikeLog'