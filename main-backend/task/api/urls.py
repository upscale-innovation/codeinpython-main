from django.urls import path
from .views import *

app_name = 'task'

urlpatterns = [
    #post
    path('create_post', CreatePostAPIView.as_view(), name='create_post'),
    path('edit_post/', PostEditAPIView.as_view(), name='edit_post'),
    path('post_list/', PostListView.as_view(), name='post_list'),
    path('delete_post/', DeletePostAPIView.as_view(), name='delete_post'),
    #bookmark
    path('bookmark/', PostBookmarkAPIView.as_view(), name='bookmark'),
    path('bookmark_list/', BookmarkListView.as_view(), name='bookmark_list'),
    #like
    path('like/', PostLikeAPIView.as_view(), name='like'),
]
