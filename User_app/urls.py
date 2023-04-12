from django.urls import path

from . import views


urlpatterns = [
    # profile 페이지 조회,수정
    path('api/profile/<int:id>', views.profile_view, name='profile'),
    path("sign-up/", views.sign_up_view, name="sign-up"),
    path("sign-in/", views.sign_in_view, name="sign-in"),
]
