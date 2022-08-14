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

class CreateCommentSerializer(ModelSerializer):
    title = serializers.CharField(error_messages={'required': "title can't be blank"})
    post = serializers.CharField(error_messages={'required': "post can't be blank"})
   
    class Meta:
        model = Comment
        fields= ['title','post']

    def validate(self, data):
        title      = data['title']
        post 	   = data['post']
        if not title or title == "":
            raise APIException400({"message":"Please provide title", "status": "False"})
        if not post or post == "":
            raise APIException400({"message":"Please provide post id", "status": "False"})
        return data

    def create(self,validated_data):
        title  = validated_data['title']
        post   = validated_data['post']
        user   = self.context['request'].user
        try:
            if (title and post):
                obj = Comment.objects.create(title=title, post_id=post, created_by=user)
                context = "A comment added by %s " % user.username
                notification = NormalNotification.objects.create(
                notification_by=user, notification_for=obj.post.created_by, notification_type='comment', 
                context=context, comment_id=obj.id)
                from_email = settings.FROM_EMAIL
                recipient_email = 'testuser@gmail.com'
                subject = context
                message = 'Comment: {}'.format(title)
                try:
                    status = send_email_task.delay(subject, message, from_email, [recipient_email, ], fail_silently=False)
                except Exception as e:
                    raise APIException400({"message": e, 'success': 'False'})
        except Exception as e:
            raise APIException400({"message":e, "status": "False"})
        return validated_data

class CreateChildCommentSerializer(ModelSerializer):
    title = serializers.CharField(error_messages={'required': "title can't be blank"})
    comment = serializers.CharField(error_messages={'required': "comment can't be blank"})
   
    class Meta:
        model = Comment
        fields= ['title','comment']

    def validate(self, data):
        title      = data['title']
        comment 	   = data['comment']
        if not title or title == "":
            raise APIException400({"message":"Please provide title", "status": "False"})
        if not comment or comment == "":
            raise APIException400({"message":"Please provide comment id", "status": "False"})
        return data

    def create(self,validated_data):
        title  = validated_data['title']
        comment   = validated_data['comment']
        user   = self.context['request'].user
        try:
            if (title and comment):
                obj = ChildComment.objects.create(title=title, comment_id=comment, created_by=user)
                context = "%s Replied to your comment " % user.username
                notification = NormalNotification.objects.create(
                notification_by=user, notification_for=obj.comment.post.created_by, notification_type='comment', 
                context=context, comment_id=obj.comment.id)
                from_email = settings.FROM_EMAIL
                recipient_email = 'testuser@gmail.com'
                subject = context
                message = 'Comment: {}'.format(title)
                try:
                    status = send_email_task.delay(subject, message, from_email, [recipient_email, ], fail_silently=False)
                except Exception as e:
                    raise APIException400({"message": e, 'success': 'False'})
        except Exception as e:
            raise APIException400({"message":e, "status": "False"})
        return validated_data


class CommentEditSerializer(ModelSerializer):
    title = CharField(allow_blank=True)
    class Meta:
        model = Comment
        fields= ['title']

    def validate(self,data):
        title = data['title'] 
        if not title or title == '':
            raise APIException400({"message":"Please provide title","status": "False"})
        return data
    def update(self, instance, validated_data):
        try:
            instance.title = validated_data.get('title', instance.title)
            instance.save()
            return instance
        except:
            raise APIException400({"message":"You are not authorized to edit","status": "False"})

class ChildCommentEditSerializer(ModelSerializer):
    title = CharField(allow_blank=True)
    class Meta:
        model = ChildComment
        fields= ['title']

    def validate(self,data):
        title = data['title'] 
        if not title or title == '':
            raise APIException400({"message":"Please provide title","status": "False"})
        return data
    def update(self, instance, validated_data):
        try:
            instance.title = validated_data.get('title', instance.title)
            instance.save()
            return instance
        except:
            raise APIException400({"message":"You are not authorized to edit","status": "False"})

class ChildCommentListSerializer(ModelSerializer):
    creator_name = SerializerMethodField()
    def get_creator_name(self, instance):
        if instance.created_by.name:
            return instance.created_by.name
        else:
            return instance.created_by.username
    class Meta:
        model = ChildComment
        fields = "__all__"

class CommentListSerializer(ModelSerializer):
    creator_name = SerializerMethodField()
    childcomment = SerializerMethodField()
    def get_childcomment(self,instance):
        qs = ChildComment.objects.filter(comment__id=instance.id)
        data = ChildCommentListSerializer(qs,many=True).data
        return data
    def get_creator_name(self, instance):
        return instance.created_by.username
    class Meta:
        model = Comment
        fields = "__all__"