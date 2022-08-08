from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.db.models import Q

from ..models import *
from account.models import User
from notification.models import *
from .serializers import *


class CreatePostAPIView(APIView):
	permisssion_classes = (IsAuthenticated,)
	def post(self,request,*args,**kwargs):
		user = request.user
		data = request.data
		serializer =  CreatePostSerializer(data=data, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response({'success' :'True','message' : 'Post created successfully','data' : serializer.data},status=200)
		return Response(serializer.errors,status=400)
        

class PostEditAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request,*args,**kwargs):
        user = request.user
        _id  = self.request.GET.get('id', None)
        try:
            obj=Post.objects.get(created_by__id=user.id, id=_id)
        except:
            return Response({'success':'False','message':'No matched record found',},status=400)
        user_qs = Post.objects.filter(created_by__id=user.id)
        if not user_qs:
            return Response({'success':'False','message' : 'Only owner can edit the post',},status=400)
        serializer =  PostEditSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj.is_edited = True
            obj.save()
            return Response({'success' :'True','message' : 'post edited successfully','data' : serializer.data},status=200)
        return Response(serializer.errors,status=400)


class PostListView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        q = self.request.GET.get('q', None)
        _id = self.request.GET.get('id', None)
        status = self.request.GET.get('status', None)
        if q:
            queryset = Post.objects.all().order_by(q)
        elif status:
            queryset = Post.objects.filter(post_status=status).distinct()
        elif (status and q):
            queryset = Post.objects.filter(post_status=status).order_by(q)
        elif _id:
            queryset = Post.objects.filter(id=_id)
        else:
            queryset = Post.objects.all()
        serializer = PostListSerializer(queryset, many=True, context={'request': request})
        data = serializer.data
        if data:
            return Response({'success': 'True','message' : 'Data retrieved successfully','data' : data,},status=200)
        else:
            return Response({'message':'No data available','success':'False'},status=400)



class DeletePostAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        user = request.user 
        _id = self.request.GET.get('id', None)
        try:
            obj=Post.objects.get(created_by__id=user.id, id=_id)
        except:
            return Response({'success' : 'False','message':'You are not authorized to delete this post',},status=400)
        if obj:
            obj.delete()
            return Response({'success' : 'True','message':'post deleted successfully'},status=200)
        else:
            return Response({'success': 'False','message':'bad request'},status=400)