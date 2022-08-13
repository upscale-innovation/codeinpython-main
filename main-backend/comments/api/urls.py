from django.urls import path
from .views import *

app_name = 'comments'

urlpatterns = [
    path('create_comment', CreateCommentAPIView.as_view(), name='create_comment'),
    path('create_childcomment', CreateChildCommentAPIView.as_view(), name='create_childcomment'),
    path('edit_comment/', CommentEditAPIView.as_view(), name='edit_comment'),
    path('edit_childcomment/', ChildCommentEditAPIView.as_view(), name='edit_childcomment'),
    path('delete_comment/', DeleteCommentAPIView.as_view(), name='delete_comment'),
    path('delete_childcomment/', DeleteChildCommentAPIView.as_view(), name='delete_childcomment'),
]
