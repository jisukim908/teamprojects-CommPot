
#api/posts/{id} urls
from django.urls import path
from . import views

urlpatterns = [
    path('api/posts/', views.post_view, name='post'),
    path('api/posts/<int:id>', views.posting_detail_view, name='detail-posting'),
    path('api/posts/delete/<int:id>',
         views.delete_posting_view, name='delete-posting'),
    path('api/posts/comment/<int:id>',
         views.write_comment_view, name='write-comment'),
    path('api/posts/comment/delete/<int:id>',
         views.delete_comment_view, name='delete-comment'),
]