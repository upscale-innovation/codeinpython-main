from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.db.models import Q

from ..models import *
from account.models import User
from notification.models import *
from .serializers import *
from vendor.task import send_email_task, send_mobile_task

class AnswerAPIView(APIView):
    permisssion_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        user = request.user
        data = request.data
        serializer =  CreateAnswerSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success' :'True','message' : 'answer created successfully','data' : serializer.data},status=200)
        return Response(serializer.errors,status=400)
    def put(self, request):
        user = request.user
        _id  = self.request.POST.get('id', None)
        try:
            obj=Answer.objects.get(id=_id)
        except:
            return Response({'success':'False','message':'No record found',},status=400)
        user_qs = Answer.objects.filter(created_by__id=user.id)
        if not user_qs:
            return Response({'success':'False','message' : 'You are not authorized to edit this Answer',},status=400)
        serializer =  AnswerEditSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            obj.is_edited = True
            obj.save()
            return Response({'success' :'True','message' : 'Answer edited successfully','data' : serializer.data},status=200)
        return Response(serializer.errors,status=400)
    def delete(self,request,*args,**kwargs):
        user = request.user 
        _id = self.request.POST.get('id', None)
        try:
            obj=Answer.objects.get(created_by__id=user.id, id=_id)
        except:
            return Response({'success' : 'False','message':'You are not authorized to delete this Answer',},status=400)
        if obj:
            try:
                notification_obj = NormalNotification.objects.get(
                Q(notification_for=obj.post.created_by) & Q(notification_by=user) & Q(notification_type='answer')& Q(answer_id=obj.id))
            except:
                return Response({'success': 'False','message':'bad request'},status=400)
            notification_obj.delete()
            obj.delete()
            return Response({'success' : 'True','message':'Answer deleted successfully'},status=200)
        return Response({'success': 'False','message':'bad request'},status=400)

#AnswerAccept Views start
class AnswerAcceptAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        data = request.data
        answer = data['answer_id']
        user = request.user
        try:
            if (user and answer):
                obj = AnswerAccept.objects.filter(answer_id=answer, created_by=user)
                if obj:
                    return Response({'success':'False','message':'answer accepted already'},status=400)
                else:
                    obj = AnswerAccept.objects.create(answer_id=answer, created_by=user)
                    context = "Your answer id: %s is accepted by the creator of the post" % answer
                    notification = NormalNotification.objects.get_or_create(
                    notification_by=user, notification_for=obj.answer.created_by, notification_type='answer_accept', 
                    context=context, answer_accept_id=obj.id)
                    to_user = obj.answer.created_by
                    if not (to_user.email):
                        message = context
                        formatted_mobile = '{}{}'.format(to_user.country_code, to_user.mobile_number)
                        try:
                            message = send_mobile_task.delay(body=message, from_='+15715172033', to=formatted_mobile)
                        except Exception as e:
                            raise APIException400({"message": e, 'success': 'False'})
                    else:
                        from_email = settings.FROM_EMAIL
                        recipient_email = to_user.email
                        subject = context
                        message = "Your answer id: %s is accepted by the creator of the post" % answer
                        try:
                            status = send_email_task.delay(subject, message, from_email, [recipient_email, ], fail_silently=False)
                        except Exception as e:
                            raise APIException400({"message": e, 'success': 'False'})
                    return Response({'success' : 'True','message':'Answer accepted successfully'},status=200)
            return Response({'success' : 'False','message':'bad request'},status=400)
        except Exception as e:
            raise APIException400({"message":e, "status": "False"})
    def delete(self, request, *args, **kwargs):
        data = request.data
        answer = data['answer_id']
        user = request.user
        if (user and answer):
            try:
                obj = AnswerAccept.objects.get(answer_id=answer, created_by=user)
            except:
                return Response({'success': 'False','message':'Answer id not exist'},status=400)
            if obj:
                try:
                    notification_obj = NormalNotification.objects.get(
                    Q(notification_for=obj.answer.created_by) & Q(notification_by=user) & 
                    Q(notification_type='answer_accept')& Q(answer_accept_id=obj.id))
                except:
                    raise APIException400({"message":'answer_accept notification id not exist', "status": "False"})
                notification_obj.delete()
                obj.delete()
                return Response({'success' : 'True','message':'answer accept removed successfully'},status=200)
        return Response({'success' : 'False','message':'bad request'},status=400)
