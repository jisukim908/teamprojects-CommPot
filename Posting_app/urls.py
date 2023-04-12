 # tweet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post, name='post'), # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('post/delete/<int:id>', views.delete_post, name='delete post'),
]