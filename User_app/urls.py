from django.urls import path
from .views import profile_view

urlpatterns = [
    # profile 페이지 조회,수정
    path('api/profile/<int:id>', profile_view, name='profile'),
]
