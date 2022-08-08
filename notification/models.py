from django.db import models
from account.models import *
from django.db.models import JSONField
from comments.models import *

# Create your models here.
NOTIFICATION_TYPE = (
		('comment', 'comment'), ('bookmark', 'bookmark'),
		('assign', 'assign'), ('mentioned', 'mentioned'))

class NormalNotification(models.Model):
	notification_by 	= models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='normal_notification_by')
	notification_for 	= models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='normal_notification_for')
	notification_type 	= models.CharField(max_length=15, blank=False, null=True, choices=NOTIFICATION_TYPE)
	context			 	= JSONField()
	created_on 			= models.DateTimeField(auto_now=True)
	read_status 		= models.BooleanField(default=False)
	comment 			= models.ForeignKey(Comment, blank=True, null=True, on_delete=models.CASCADE, related_name='commentor')