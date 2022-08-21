from rest_framework import serializers
from rest_framework.serializers import *
from ..models import *
from django.db.models import Q
from common_utils.exception import APIException400
from django.utils.timezone import now
from datetime import datetime
from comments.api.serializers import *
from comments.models import *
# from account.api.serializers import (UserSerializer,)
from account.models import User
from answer.models import *
from answer.api.serializers import *

#Post Serializer
class CreatePostSerializer(ModelSerializer):
    title = serializers.CharField(error_messages={'required': "title can't be blank"})
    description = serializers.CharField(error_messages={'required': "description can't be blank"})
    # image = serializers.ListField(error_messages={'required': "image key is required", 'blank': "image key can't be blank"},
    #                                         child=serializers.ImageField(error_messages={'required': "image key is required", 'blank': "image key can't be blank"}))
    class Meta:
        model = Post
        fields= ['title','description']

    def validate(self, data):
        title              = data['title']
        description 	   = data['description']
        if not title or title == "":
            raise APIException400({"message":"Please provide title", "status": "False"})
        if not description or description == "":
            raise APIException400({"message":"Please provide description", "status": "False"})
        return data
    def create(self,validated_data):
        title        = validated_data['title']
        description        = validated_data['description']
        user = self.context['request'].user
        if (title and description):
            post_obj = Post.objects.create(
			    title=title, description=description, created_by=user) 
        if 'file' in (self.context['request'].FILES):
            file = (self.context['request'].FILES).getlist('file')
            PostFile.objects.bulk_create([PostFile(post=post_obj,file=i) for i in file])
        return validated_data


class PostEditSerializer(ModelSerializer):
    title = CharField(allow_blank=True)
    description = CharField(allow_blank=True)
    class Meta:
        model = Post
        fields= ['title', 'description']

    def validate(self,data):
        title = data['title']
        description = data['description']    
        if not (title or description):
            raise APIException400({"message":"Please provide either title or description","status": "False"})
        return data
    def update(self, instance, validated_data):
        if not (validated_data['title'] == "" or validated_data['title'] is None):
            instance.title = validated_data.get('title', instance.title)
        if not (validated_data['description'] == "" or validated_data['description'] is None):
            instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class PostFilesSerializer(ModelSerializer):
	class Meta:
		model = PostFile
		fields = ['file']

class CategorySerializer(ModelSerializer):
	class Meta:
		model = Category
		fields = "__all__"

class PostListSerializer(ModelSerializer):
    files = SerializerMethodField()
    comment = SerializerMethodField()
    answer = SerializerMethodField()
    def get_files(self,instance):
        qs = PostFile.objects.filter(post__id=instance.id)
        data = PostFilesSerializer(qs,many=True).data
        return data
    def get_comment(self,instance):
        qs = Comment.objects.filter(post__id=instance.id)
        data = CommentListSerializer(qs,many=True).data
        return data
    def get_answer(self,instance):
        qs = Answer.objects.filter(post__id=instance.id)
        data = AnswerSerializer(qs,many=True).data
        return data
    categories = CategorySerializer(many=True)
    class Meta:
        model = Post
        fields = "__all__"

class ElasticUserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name')

class ElasticPostListSerializer(ModelSerializer):
    created_by = ElasticUserSerializer()
    categories = CategorySerializer(many=True)
    class Meta:
        model = Post
        fields = "__all__"


#Bookmark serializer
class BookmarkListSerializer(ModelSerializer):
    post_title = SerializerMethodField()
    post_description = SerializerMethodField()
    post_id = SerializerMethodField()
    def get_post_title(self, instance):
        if instance.post.title:
            return instance.post.title
    def get_post_description(self, instance):
        if instance.post.description:
            return instance.post.description
    def get_post_id(self, instance):
        if instance.post.id:
            return instance.post.id
    class Meta:
        model = PostBookmark
        fields = "__all__"


