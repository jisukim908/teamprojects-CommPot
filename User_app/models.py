from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# Create your User here.

# Create your Profile here.


class Profile(models.Model):
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
