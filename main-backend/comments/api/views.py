from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.db.models import Q

from ..models import *
from account.models import User
from notification.models import *
from .serializers import *


class CreateCommentAPIView(APIView):
	permisssion_classes = (IsAuthenticated,)
	def post(self,request,*args,**kwargs):
		user = request.user
		data = request.data
		serializer =  CreateCommentSerializer(data=data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response({'success' :'True','message' : 'comment created successfully','data' : serializer.data},status=200)
		return Response(serializer.errors,status=400)

class CreateChildCommentAPIView(APIView):
	permisssion_classes = (IsAuthenticated,)
	def post(self,request,*args,**kwargs):
		user = request.user
		data = request.data
		serializer =  CreateChildCommentSerializer(data=data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response({'success' :'True','message' : 'child comment created successfully','data' : serializer.data},status=200)
		return Response(serializer.errors,status=400)


class CommentEditAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request,*args,**kwargs):
        user = request.user
        _id  = self.request.GET.get('id', None)
        try:
            obj=Comment.objects.get(created_by__id=user.id, id=_id)
        except:
            return Response({'success':'False','message':'No record found',},status=400)
        user_qs = Comment.objects.filter(created_by__id=user.id)
        if not user_qs:
            return Response({'success':'False','message' : 'You are not authorized to edit this comment',},status=400)
        serializer =  CommentEditSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj.is_edited = True
            obj.save()
            return Response({'success' :'True','message' : 'comment edited successfully','data' : serializer.data},status=200)
        return Response(serializer.errors,status=400)


class ChildCommentEditAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request,*args,**kwargs):
        user = request.user
        _id  = self.request.GET.get('id', None)
        try:
            obj=ChildComment.objects.get(created_by__id=user.id, id=_id)
        except:
            return Response({'success':'False','message':'No record found',},status=400)
        user_qs = ChildComment.objects.filter(created_by__id=user.id)
        if not user_qs:
            return Response({'success':'False','message' : 'You are not authorized to edit this comment',},status=400)
        serializer =  ChildCommentEditSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj.is_edited = True
            obj.save()
            return Response({'success' :'True','message' : 'child comment edited successfully','data' : serializer.data},status=200)
        return Response(serializer.errors,status=400)


class DeleteCommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        user = request.user 
        _id = self.request.GET.get('id', None)
        try:
            obj=Comment.objects.get(created_by__id=user.id, id=_id)
        except:
            return Response({'success' : 'False','message':'You are not authorized to delete this comment',},status=400)
        if obj:
            try:
                notification_obj = NormalNotification.objects.get(
                Q(notification_for=obj.post.created_by) & Q(notification_by=user) & Q(notification_type='comment')& Q(comment_id=obj.id))
            except:
                return Response({'success': 'False','message':'bad request'},status=400)
            notification_obj.delete()
            obj.delete()
            return Response({'success' : 'True','message':'comment deleted successfully'},status=200)
        return Response({'success': 'False','message':'bad request'},status=400)


class DeleteChildCommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        user = request.user 
        _id = self.request.GET.get('id', None)
        try:
            obj=ChildComment.objects.get(created_by__id=user.id, id=_id)
        except:
            return Response({'success' : 'False','message':'You are not authorized to delete this child comment',},status=400)
        if obj:
            try:
                notification_obj = NormalNotification.objects.get(
                Q(notification_for=obj.comment.post.created_by) & Q(notification_by=user) & Q(notification_type='comment')& Q(comment_id=obj.comment.id))
            except:
                return Response({'success': 'False','message':'bad request'},status=400)
            notification_obj.delete()
            obj.delete()
            return Response({'success' : 'True','message':'child comment deleted successfully'},status=200)
        return Response({'success': 'False','message':'bad request'},status=400)