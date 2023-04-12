# user/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# Create your models here.
# Create your User here.
class UserModel(models.Model):
    class Meta:
        db_table = "my_user"

    username = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=256, null=False)
    bio = models.CharField(max_length=256, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
# Create your Profile here.


class Profile(models.Model):
    '''
    프로필. 거주지역과 생성일, 수정일,
    '''
    class Meta:
        db_table = 'profile'
    username = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, to_field="username")
    locate = models.CharField(verbose_name='region',
                              max_length=16, default='Not specified')
    description = models.TextField(max_length=300,)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    # profile_image=models.ImageField(,)
