from django.urls import path

from . import views


urlpatterns = [
    # profile 페이지 조회,수정
    path('api/profile/<str:path_username>',
         views.profile_view, name='profile'),
    path("api/user/signup/", views.sign_up_view, name="sign-up"),
    path("api/user/login/", views.sign_in_view, name="login"),
    path("api/user/logout/", views.logout_view, name="logout"),
    path("api/user/follow/<str:path_username>",
         views.user_follow_view, name='follow'),
    path("api/user/delete/", views.delete_account_view, name='delete-acount')

]
