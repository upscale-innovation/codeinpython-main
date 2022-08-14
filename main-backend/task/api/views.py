from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from twilio.rest import Client
import os,sys

from ..models import *
from account.models import User
from notification.models import *
from .serializers import *
from common_utils.exception import APIException400
from vendor.task import send_email_task, send_mobile_task

try:  
   account_sid = os.getenv('account_sid')
   auth_token =  os.getenv('SECRET_KEY')
except KeyError: 
   print("Please set the environment variable of account_sid and auth_token")
   sys.exit(1)

#Post VIews start
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
        if request.user.is_authenticated:
            for i in data:
                _id = i['id']
                l_qs = PostLike.objects.filter(Q(post_id__id=_id) & Q(liked_by=request.user))
                b_qs = PostBookmark.objects.filter(Q(post_id__id=_id) & Q(bookmark_by=request.user))
                if l_qs.count() >= 1:
                    i['is_liked'] = True
                else:
                    i['is_liked'] = False
                if b_qs.count() >= 1:
                    i['is_bookmarked'] = True
                else:
                    i['is_bookmarked'] = False
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


#Bookmark Views start
class PostBookmarkAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        data = request.data
        post = data['post_id']
        user = request.user
        types =  self.request.POST.get('type', None)
        #types to check bookmark is add or remove
        if types == 'add':
            try:
                if (user and post):
                    obj = PostBookmark.objects.filter(post_id=post, bookmark_by=user)
                    if obj:
                        return Response({'success':'True','message':'post bookmarked already'},status=400)
                    else:
                        obj = PostBookmark.objects.create(post_id=post, bookmark_by=user)
                        context = "bookmarked by %s " % user.username
                        notification = NormalNotification.objects.get_or_create(
                        notification_by=user, notification_for=obj.post.created_by, notification_type='bookmark', 
                        context=context, bookmark_id=obj.id)
                        if not (user.email):
                            message = 'You added the bookmarked of this post'
                            formatted_mobile = '{}{}'.format(user.country_code, user.mobile_number)
                            client = Client(account_sid, auth_token)
                            try:
                                message = send_mobile_task.delay(body=message, from_='+15715172033', to=formatted_mobile)
                            except Exception as e:
                                raise APIException400({"message": e, 'success': 'False'})
                        else:
                            from_email = settings.FROM_EMAIL
                            recipient_email = user.email
                            subject = context
                            message = 'You added the bookmarked of this post'
                            try:
                                status = send_email_task.delay(subject, message, from_email, [recipient_email, ], fail_silently=False)
                            except Exception as e:
                                raise APIException400({"message": e, 'success': 'False'})
                        return Response({'success' : 'True','message':'bookmarked successfully'},status=200)
                return Response({'success' : 'True','message':'bad request'},status=400)
            except Exception as e:
                raise APIException400({"message":e, "status": "False"})
        elif types == 'remove':
            if (user and post):
                try:
                    obj = PostBookmark.objects.get(post_id=post, bookmark_by=user)
                except:
                    return Response({'success': 'False','message':'bookmark id not exist'},status=400)
                if obj:
                    try:
                        notification_obj = NormalNotification.objects.get(
                        Q(notification_for=obj.post.created_by) & Q(notification_by=user) & 
                        Q(notification_type='bookmark')& Q(bookmark_id=obj.id))
                    except:
                        raise APIException400({"message":'bookmark notification id not exist', "status": "False"})
                    notification_obj.delete()
                    obj.delete()
                    return Response({'success' : 'True','message':'bookmark removed successfully'},status=200)
            return Response({'success' : 'True','message':'bad request'},status=200)
        raise APIException400({"message":'bad request on types', "status": "False"})



class BookmarkListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        q = self.request.GET.get('q', None)
        _id = self.request.GET.get('id', None)
        user = request.user
        if q:
            queryset = PostBookmark.objects.all().order_by(q)
        elif _id:
            queryset = PostBookmark.objects.filter(id=_id)
        else:
            queryset = PostBookmark.objects.all()
        serializer = BookmarkListSerializer(queryset, many=True, context={'request': request})
        data = serializer.data
        if data:
            return Response({'success': 'True','message' : 'Data retrieved successfully','data' : data,},status=200)
        else:
            return Response({'message':'No data available','success':'False'},status=400)


#PostViews start
class PostLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        data = request.data
        post = data['post_id']
        user = request.user
        types =  self.request.POST.get('type', None)
        if types == 'add':
            try:
                if (user and post):
                    obj = PostLike.objects.filter(post_id=post, liked_by=user)
                    if obj:
                        return Response({'success':'True','message':'post liked already'},status=400)
                    else:
                        obj = PostLike.objects.create(post_id=post, liked_by=user)
                        context = "liked by %s " % user.username
                        notification = NormalNotification.objects.get_or_create(
                        notification_by=user, notification_for=obj.post.created_by, notification_type='like', 
                        context=context, like_id=obj.id)
                        return Response({'success' : 'True','message':'likeed successfully'},status=200)
                return Response({'success' : 'True','message':'bad request'},status=400)
            except Exception as e:
                raise APIException400({"message":e, "status": "False"})
        elif types == 'remove':
            if (user and post):
                try:
                    obj = PostLike.objects.get(post_id=post, liked_by=user)
                except:
                    return Response({'success': 'False','message':'like id not exist'},status=400)
                if obj:
                    try:
                        notification_obj = NormalNotification.objects.get(
                        Q(notification_for=obj.post.created_by) & Q(notification_by=user) & 
                        Q(notification_type='like')& Q(like_id=obj.id))
                    except:
                        raise APIException400({"message":'like notification id not exist', "status": "False"})
                    notification_obj.delete()
                    obj.delete()
                    return Response({'success' : 'True','message':'like removed successfully'},status=200)
            return Response({'success' : 'True','message':'bad request'},status=200)
        raise APIException400({"message":'bad request on types', "status": "False"})

