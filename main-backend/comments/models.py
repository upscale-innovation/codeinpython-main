from django.db import models

# Create your models here.
from account.models import User
from task.models import Post
from django.utils.timezone import now

class Comment(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    is_edited = models.BooleanField(default=False)

    class Meta:
        unique_together = ('id', 'created_on')

class ChildComment(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='childcomment_created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='childcomment_comment')
    is_edited = models.BooleanField(default=False)

    class Meta:
        unique_together = ('id', 'created_on')