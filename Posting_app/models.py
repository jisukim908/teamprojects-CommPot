
# tweet/models.py
from django.db import models

from User_app.models import UserModel


# Create your models here.


class Posting(models.Model):
    class Meta:
        db_table = "posting"
    CATEGORIES = (
        ('recipe', 'Recipes'),
        ('recommend', 'Recommendation'),
        ('chat', 'Chat'),
    )

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name='글 제목')
    content = models.TextField(verbose_name='글 내용')
    category = models.CharField(
        choices=CATEGORIES, max_length=9, verbose_name='카테고리')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostingComment(models.Model):
    class Meta:
        db_table = "comment"
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
