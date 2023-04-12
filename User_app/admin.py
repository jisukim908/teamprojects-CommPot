from django.contrib import admin
from .models import UserModel

# 나의 UserModel을 Admin에 추가
admin.site.register(UserModel)
