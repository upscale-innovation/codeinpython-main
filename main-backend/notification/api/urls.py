from django.urls import path
from .views import *

app_name = 'notifications_api'

urlpatterns = [

    path('notify_for_user', NormalNotificationForUserAPIView.as_view(), name='notify_for_user'),
    path('user_unread_notification', UnreadNotificationByUserAPIView.as_view(), name='user_unread_notification'),
]