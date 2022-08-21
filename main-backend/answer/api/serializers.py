from rest_framework import serializers
from rest_framework.serializers import *
from ..models import *
from django.db.models import Q
from common_utils.exception import APIException400
from django.utils.timezone import now
from datetime import datetime
from notification.models import *
from django.conf import settings
from django.core.mail import send_mail
from vendor.task import send_email_task

class CreateAnswerSerializer(ModelSerializer):
    content = serializers.CharField(error_messages={'required': "content can't be blank"})
    post = serializers.CharField(error_messages={'required': "post can't be blank"})
    class Meta:
        model = Answer
        fields= ['content','post']
    def validate(self, data):
        content      = data['content']
        post 	   = data['post']
        if not content or content == "":
            raise APIException400({"message":"Please provide content", "status": "False"})
        if not post or post == "":
            raise APIException400({"message":"Please provide post id", "status": "False"})
        return data
    def create(self,validated_data):
        content  = validated_data['content']
        post   = validated_data['post']
        user   = self.context['request'].user
        try:
            if (content and post):
                obj = Answer.objects.create(content=content, post_id=post, created_by=user)
                context = "An answer added by %s " % user.username
                notification = NormalNotification.objects.create(
                notification_by=user, notification_for=obj.post.created_by, notification_type='answer', 
                context=context, answer_id=obj.id)
                from_email = settings.FROM_EMAIL
                recipient_email = 'testuser@gmail.com'
                subject = context
                message = 'Answer: {}'.format(content)
                try:
                    status = send_email_task.delay(subject, message, from_email, [recipient_email, ], fail_silently=False)
                except Exception as e:
                    raise APIException400({"message": e, 'success': 'False'})
        except Exception as e:
            raise APIException400({"message":e, "status": "False"})
        return validated_data


class AnswerEditSerializer(ModelSerializer):
    content = CharField(allow_blank=True)
    class Meta:
        model = Answer
        fields= ['content']
    def validate(self,data):
        content = data['content'] 
        if not content or content == '':
            raise APIException400({"message":"Please provide content","status": "False"})
        return data
    def update(self, instance, validated_data):
        try:
            instance.content = validated_data.get('content', instance.content)
            instance.save()
            return instance
        except:
            raise APIException400({"message":"You are not authorized to edit","status": "False"})

class AnswerSerializer(ModelSerializer):
    creator = SerializerMethodField()
    answer_accepted = SerializerMethodField()
    def get_creator(self, instance):
        if instance.created_by.first_name:
            return instance.created_by.first_name
        else:
            return instance.created_by.username
    def get_answer_accepted(self, instance):
        qs = AnswerAccept.objects.filter(answer_id=instance.id)
        if qs.count() >= 1:
            answer_accepted = True
            return answer_accepted
        else:
            answer_accepted = False
            return answer_accepted
    class Meta:
        model = Answer
        fields = "__all__"


