from django.db import models

# Create your models here.
from account.models import User
from task.models import Post
from django.utils.timezone import now

class Comment(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_edited = models.BooleanField(default=False)

    class Meta:
        unique_together = ('id', 'created_on')