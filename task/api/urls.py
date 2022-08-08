from django.urls import path
from .views import *

app_name = 'task'

urlpatterns = [
    path('create_post', CreatePostAPIView.as_view(), name='create_post'),
    path('edit_post/', PostEditAPIView.as_view(), name='edit_post'),
    path('post_list/', PostListView.as_view(), name='post_list'),
    path('delete_post/', DeletePostAPIView.as_view(), name='delete_post'),
]
