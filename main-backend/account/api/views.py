import code

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import *
from ..models import *
from datetime import timedelta, datetime
import uuid
from django.utils.timezone import make_aware
from django.core.mail import send_mail
from vendor.task import send_email_task,send_mobile_task
from django.conf import settings
from twilio.rest import Client
from common_utils.exception import APIException400
from common_utils.generate_otp import generateOTP

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

try:  
   account_sid = os.getenv('account_sid')
   auth_token =  os.getenv('SECRET_KEY')
except KeyError: 
   print("Please set the environment variable of account_sid and auth_token")
   sys.exit(1)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': "Registration successful",
                'data': serializer.data,
                'success': True
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0],'success': False}, status=400)
        return Response(serializer.errors, status=400)


class LogInUser(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LogInUserSerializer

    def post(self, request, *args, **kwargs):
        import logging
        data = request.data
        logger = logging.getLogger('accounts')
        logger.info('inside post')
        logger.info(data)
        serializer = LogInUserSerializer(data=request.data)
        if serializer.is_valid():
            logger.info('serializer is valid')
            logger.info(data)
            return Response({'message': "Login Successful", 'data': serializer.data,'success': True}, status=200, )
        else:
            error_keys = list(serializer.errors.keys())
            if error_keys:
                error_msg = serializer.errors[error_keys[0]]
                return Response({'message': error_msg[0]}, status=400)
            return Response(serializer.errors, status=400)



class ForgetPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': "OTP sent successfully",'data': serializer.data,'success': True}, status=200, )
        else:
            error_keys = list(serializer.errors.keys())
            if error_keys:
                error_msg = serializer.errors[error_keys[0]]
                return Response({'message': error_msg[0]}, status=400)
            return Response(serializer.errors, status=400)


class ResendOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if 'mobile_number' not in data or data['mobile_number'] == '':
            raise APIException400({"message": "mobile_number key is required"})
        mobile_number = data['mobile_number']
        if not mobile_number.isdigit():
            if len(mobile_number.split('@')) < 2:
                raise APIException400({"message": "Invalid email"})
            email = mobile_number
            user_obj = User.objects.filter(email=mobile_number)
            if not user_obj.exists():
                raise APIException400({"message": 'user does not exist with this email', 'success': 'False'})
        else:
            if 'country_code' not in data or data['country_code'] == '':
                raise APIException400({"message": "country code is required"})
            email = None
            country_code = data['country_code']
            if not country_code.split('+')[1].isdigit():
                raise APIException400({"message": "Invalid Country Code"})
            user_obj = User.objects.filter(mobile_number=mobile_number, country_code=country_code)
            if not user_obj.exists():
                raise APIException400({"message": 'user does not exist with this mobile number', 'success': 'False'})

        if not email:
            user = User.objects.get(mobile_number=mobile_number, country_code=country_code)
            code = generateOTP()
            current_time = make_aware(datetime.now())
            expire_time = current_time + timedelta(minutes=30)
            otp_created = OTPStorage.objects.create(otp=code, user=user, created=expire_time)
            otp_created.save()
            subject = 'OTP verification'
            message = 'Your One Time Password For Verification is : {}'.format(code)
            formatted_mobile = '{}{}'.format(country_code, mobile_number)
            client = Client(account_sid, auth_token)
            try:
                message = send_mobile_task.delay(body=message, from_='+15715172033', to=formatted_mobile)
            except Exception as e:
                raise APIException400({"message": e, 'success': 'False'})
            return Response(
                {'success': 'True', 'message': 'OTP resend successfully to your registered mobile number', "OTP":code},
                status=200)
        else:
            user = User.objects.get(email=email)
            code = generateOTP()
            current_time = make_aware(datetime.now())
            expire_time = current_time + timedelta(minutes=30)
            otp_created = OTPStorage.objects.create(otp=code, user=user, created=expire_time)
            otp_created.save()
            from_email = settings.FROM_EMAIL
            recipient_email = email
            subject = 'OTP verification mail'
            message = 'Your One Time Password For Verification is : {}'.format(code)
            try:
                status = send_email_task.delay(subject, message, from_email, [recipient_email, ], fail_silently=False)
            except Exception as e:
                raise APIException400({"message": e, 'success': 'False'})
            return Response({'success': 'True', 'message': 'OTP resend successfully to your registered email id', "OTP":code},
                            status=200)


class VerifyOTP(RetrieveAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if 'mobile_number' not in data or data['mobile_number'] == '':
            raise APIException400({"message": "mobile number is required"})
        mobile_number = data['mobile_number']
        if not mobile_number.isdigit():
            if len(mobile_number.split('@')) < 2:
                raise APIException400({"message": "Invalid email"})
            email = mobile_number
        else:
            if 'country_code' not in data or data['country_code'] == '':
                raise APIException400({"message": "country code is required"})
            email = None
            country_code = data['country_code']
            if not country_code.split('+')[1].isdigit():
                raise APIException400({"message": "Invalid Country Code"})
        try:
            if not email:
                user = User.objects.get(mobile_number=mobile_number, country_code=country_code)
            else:
                user = User.objects.get(email=email)
        except:
            raise APIException400({"message": "User with this mobile credential doesn't exists"})
        if user.mobile_number is None:
            obj_qs = User.objects.filter(email__iexact=user.email)
            if obj_qs.exists() and obj_qs.count() == 1:
                user_obj = obj_qs.first()
                current_time = make_aware(datetime.now())
                otp_obj = OTPStorage.objects.filter(user=user_obj, otp=data['otp'], is_used=False,
                                                    created__gt=current_time).first()
                if otp_obj:
                    otp_obj.is_used = True
                    otp_obj.save()
                    user.email_verified = True
                    user.save()
                    payload = jwt_payload_handler(user_obj)
                    token = jwt_encode_handler(payload)
                    token = 'JWT ' + str(token)
                    return Response({"message": "email OTP Verification success", 'token': token,'success': 'True'})
                return Response({'success': 'False', 'message': 'Invalide verification code'}, status=400)
            return Response({'success': 'False', 'message': 'user does not exist with this email'}, status=400)
        else:
            obj_qs = User.objects.filter(mobile_number__iexact=user.mobile_number)
            if obj_qs.exists() and obj_qs.count() == 1:
                user_obj = obj_qs.first()
                current_time = make_aware(datetime.now())
                otp_obj = OTPStorage.objects.filter(user=user_obj, otp=data['otp'], is_used=False,
                                                    created__gt=current_time).first()
                if otp_obj:
                    otp_obj.is_used = True
                    otp_obj.save()
                    user.mobile_verified = True
                    user.save()
                    payload = jwt_payload_handler(user_obj)
                    token = jwt_encode_handler(payload)
                    token = 'JWT ' + str(token)
                    return Response({"message": "mobile OTP Verification success", 'token': token,'success': 'True'})
                return Response({'success': 'False', 'message': 'Invalide verification code'}, status=400)
            return Response({'success': 'False', 'message': 'user does not exist with this mobile'}, status=400)


class ResetPasswordResetAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JSONWebTokenAuthentication, ]
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid():
            new_password = serializer.data.get("new_password")
            confirm_password = serializer.data.get("confirm_password")
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return Response({'success': "true", 'message': 'Your password has been reset successfully'},
                                status=200)
            return Response({'success': "False", 'message': 'Both password fields must be same'}, status=400)
        return Response(serializer.errors, status=400)


class UserProfileEditAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request,*args,**kwargs):
        user = request.user
        _id  = self.request.GET.get('id', None)
        try:
            obj=UserProfile.objects.get(user__id=user.id, id=_id)
        except:
            return Response({'success':'False','message':'No matched record found',},status=400)
        user_qs = UserProfile.objects.filter(user__id=user.id)
        if not user_qs:
            return Response({'success':'False','message' : 'Only owner can edit his/her profile',},status=400)
        serializer =  UserProfileEditSerializer(obj,data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            obj.save()
            return Response({'success' :'True','message' : 'profile edited successfully','data' : serializer.data},status=200)
        return Response(serializer.errors,status=400)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user_id = self.request.GET.get('username', None)
        user = request.user
        if user_id:
            try:
                queryset = User.objects.filter(username=user_id)
            except Exception as e:
                raise APIException400({"message": "user does not exist with this username"})
        else:
            return Response({'message':'username is required','success':'False'},status=400)
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        data = serializer.data
        if data:
            return Response({'success': 'True','message' : 'Data retrieved successfully','data' : data,},status=200)
        return Response({'message':'No data available','success':'False'},status=400)


class TotalUsersView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        filter = self.request.GET.get('filter', None)
        user = request.user
        if filter:
            queryset = User.objects.all().order_by(filter)
        else:
            queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        data = serializer.data
        if data:
            return Response({'success': 'True','message' : 'Data retrieved successfully','data' : data,},status=200)
        return Response({'message':'No data available','success':'False'},status=400)