from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator
# Create your models here.


class Users(models.Model):
    user = models.OneToOneField(User)
    number = models.BigIntegerField()

    def __str__(self):
        return self.user.get_short_name() 


class Article(models.Model):
    text = models.TextField(max_length=10000)
    title = models.CharField(max_length=200)
    link = models.TextField(max_length=10000)
    published = models.DateField()
    cat = models.TextField(max_length=10000, null=True)
    imagelink = models.TextField(max_length=10000, null=True)


class Comment(models.Model):
    user = models.ForeignKey(Users, related_name = '%(class)s_UserFK')
    article = models.ForeignKey(Article, related_name = '%(class)s_ArticleFK', null=True)
    text = models.TextField()
    Date = models.DateField()


class Like(models.Model):
    article = models.ForeignKey(Article, related_name = '%(class)s_ArticleFK', null = True)
    UserFK = models.ForeignKey(Users, related_name = '%(class)s_UserFK')
    likeOrDislike = models.BooleanField()
