from rest_framework import serializers
from rest_framework.serializers import *
from ..models import *
from django.db.models import Q
from account.exception import APIException400
from django.utils.timezone import now
from datetime import datetime
from notification.models import *



class CreateCommentSerializer(ModelSerializer):
    title = serializers.CharField(error_messages={'required': "title can't be blank"})
    post = serializers.CharField(error_messages={'required': "description can't be blank"})
   
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


class CommentListSerializer(ModelSerializer):
    creator_name = SerializerMethodField()
    def get_creator_name(self, instance):
        if instance.created_by.name:
            return instance.created_by.name
        else:
            return instance.created_by.username
    class Meta:
        model = Comment
        fields = "__all__"