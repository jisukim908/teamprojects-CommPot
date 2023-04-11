from django.db import models
from user.models import UserModel

# Create your models here.
class Posting(models.Model):
    class Meta:
        db_table = "posting"
    
author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
title = models.CharField(max_length=50)
content = models.CharField()
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)