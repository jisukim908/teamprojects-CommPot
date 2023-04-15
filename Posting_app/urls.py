
# api/posts/{id} urls
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/posts/search', views.search, name='search'),
    path('api/posts/', views.post_view, name='post'),
    path('api/posts/<int:id>', views.posting_detail_view, name='detail-posting'),
    path('api/posts/edit/<int:id>', views.posting_edit_view, name='edit-posting'),
    path('api/posts/delete/<int:id>',
         views.delete_posting_view, name='delete-posting'),
    path('api/posts/comment/<int:id>',
         views.write_comment_view, name='write-comment'),
    path('api/posts/comment/modify/<int:id>',
         views.comment_modify_view, name='modify-comment'),
    path('api/posts/comment/delete/<int:id>',
         views.delete_comment_view, name='delete-comment'),

]
