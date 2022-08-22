from django.db import models
from account.models import User
from task.models import Post

# Create your models here.


class Answer(models.Model):
    content = models.TextField(max_length=2000, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_creator')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='answer_post')
    is_edited = models.BooleanField(default=False)

    class Meta:
        unique_together = ('id', 'created_on')

    def __str__(self):
        return f'{self.id}: {self.created_by.username} ({self.created_on.date()})'


class AnswerAccept(models.Model):
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE, related_name='answer_accept')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_accept_creator')
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('id', 'created_on')

    def __str__(self):
        return f'{self.id}: {self.created_by.username} ({self.created_on.date()})'