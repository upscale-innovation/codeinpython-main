from django.urls import path
from .views import *

app_name = 'answer'

urlpatterns = [
    path('answer', AnswerAPIView.as_view(), name='answer'),
    path('answer_accept', AnswerAcceptAPIView.as_view(), name='answer_accept'),
]
