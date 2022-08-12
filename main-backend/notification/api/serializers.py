from rest_framework import serializers
from rest_framework.serializers import *
from ..models import *

class NormalNotificationSerializer(ModelSerializer):
	class Meta:
		model = NormalNotification 
		fields = "__all__"

