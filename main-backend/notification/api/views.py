from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.db.models import Q

from ..models import *
from .serializers import *


class NormalNotificationForUserAPIView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request,*args,**kwargs):
		user = request.user
		queryset = NormalNotification.objects.filter(notification_for=user).order_by('-created_on')
		serializer = NormalNotificationSerializer(queryset, many=True, context={'request': request})
		data = serializer.data
		total_result = queryset.count()
		queryset.update(read_status=True)

		if data:
			return Response({'success' : 'True','message' : 'Data retrieved successfully',
				'total_result'  :total_result, 'data': data,},status=200)
		else:
			return Response({'message':'No data to retrieve','success':'False'},status=400)


class UnreadNotificationByUserAPIView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request,*args,**kwargs):
		user = request.user
		unread_notification_qs = NormalNotification.objects.filter(Q(notification_for=user) & Q(read_status=0)).count()
		return Response({
			'success' : 'True',
			'message' : 'Data retrieved successfully',
			'unread_notification':unread_notification_qs,
		},status=200)

