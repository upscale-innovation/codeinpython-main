from django.db.models import Q
from rest_framework.serializers import *
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from ..models import *
from task.models import *
from comments.models import *
from task.api.serializers import (PostListSerializer,)
from comments.api.serializers import (CommentListSerializer,)
from common_utils.exception import APIException400
from common_utils.generate_otp import generateOTP

from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
import os,sys
from vendor.task import send_email_task, send_mobile_task

try:  
   account_sid = os.getenv('account_sid')
   auth_token =  os.getenv('auth_token')
except KeyError: 
   print("Please set the environment variable of account_sid and auth_token")
   sys.exit(1)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(error_messages={'required': "name can't be blank"})
    country_code = serializers.CharField(error_messages={'required': "country code can't be blank"})
    mobile_number = serializers.CharField(
        error_messages={'required': "mobile_number key is required", 'blank': "mobile_number key can't be blank"})
    password = serializers.CharField(write_only=True, required=False,
                error_messages={'blank': "password key can't be blank"})
    authorization = serializers.CharField(read_only=True)
    mobile_verified = serializers.BooleanField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    def validate(self, attrs):
        country_code = attrs['country_code']
        mobile_number = attrs['mobile_number']

        if not mobile_number.isdigit():
            if len(mobile_number.split('@')) < 2:
                raise APIException400({"message": "Invalid email"})
            email = mobile_number
            if User.objects.filter(email=mobile_number).exists():
                raise APIException400({"message": "This email already exists. Please login"})
        else:
            if 'country_code' not in attrs:
                raise APIException400({"message": "country code is required"})
            email = None
            country_code = attrs['country_code']
            if not country_code.split('+')[1].isdigit():
                raise APIException400({"message": "Invalid Country Code"})
            if User.objects.filter(mobile_number=mobile_number).exists():
                raise APIException400({"message": "This mobile_number already exists. Please login"})
            if 'password' not in attrs:
                raise APIException400({'error_message': "Password is required"})
            password = attrs['password']
            if len(password) < 8:
                raise APIException400({'message': "Password must be of atleast 8 characters"})
        return attrs

    def create(self, validated_data):
        mobile_number = validated_data['mobile_number']
        name = validated_data['name']
        if not mobile_number.isdigit():
            if len(mobile_number.split('@')) < 2:
                raise APIException400({"message": "Invalid email"})
            email = mobile_number
            try:
                user = User.objects.create(username=email, email=mobile_number, mobile_number=None, country_code=None)
                user_profile = UserProfile.objects.create(name=name,user=user)
                user.set_password(validated_data['password'])
                user.save()
                user_profile.save()
            except Exception as e:
                raise APIException400({'message': e})
        else:
            if 'country_code' not in validated_data:
                raise APIException400({"message": "country code is required"})
            email = None
            country_code = validated_data['country_code']
            if not country_code.split('+')[1].isdigit():
                raise APIException400({"message": "Invalid Country Code"})
            try:
                user = User.objects.create(username=mobile_number, mobile_number=mobile_number, email=None,
                                        country_code=validated_data['country_code'])
                user_profile = UserProfile.objects.create(name=name,user=user)
                user.set_password(validated_data['password'])
                user.save()
                user_profile.save()
            except Exception as e:
                raise APIException400({'message': e})
        payload = jwt_payload_handler(user)
        token = 'JWT ' + jwt_encode_handler(payload)
        validated_data['authorization'] = token
        return validated_data


class LogInUserSerializer(serializers.Serializer):
    country_code = serializers.CharField(required=False, error_messages={'blank': "country code can't be blank"})
    mobile_number = serializers.CharField(
        error_messages={'required': "mobile number is required", 'blank': "mobile number can't be blank"})
    password = serializers.CharField(required=False, write_only=True,
                                     error_messages={'blank': "Password can't be blank"})
    authorization = serializers.CharField(read_only=True)
    mobile_verified = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)
    user_id = serializers.CharField(read_only=True)

    def validate(self, attrs):
        mobile_number = attrs['mobile_number']

        if not mobile_number.isdigit():
            if len(mobile_number.split('@')) < 2:
                raise APIException400({"message": "Invalid email"})
            email = mobile_number
        else:
            if 'country_code' not in attrs:
                raise APIException400({"message": "country code is required"})
            email = None
            country_code = attrs['country_code']
            if not country_code.split('+')[1].isdigit():
                raise APIException400({"message": "Invalid Country Code"})
        try:
            if not email:
                user = User.objects.get(mobile_number=mobile_number, country_code=country_code)
            else:
                user = User.objects.get(email=email)
        except:
            raise APIException400({"message": "Email or Mobile Number doesn't exist. Please register first"})
        if 'password' not in attrs or attrs['password'] == '':
            raise APIException400({"message": "Please provide Password"})
        if not user.check_password(attrs['password']):
            raise APIException400({"message": "Invalid Password"})
        user.save()
        payload = jwt_payload_handler(user)
        token = 'JWT ' + jwt_encode_handler(payload)
        attrs['authorization'] = token
        attrs['mobile_verified'] = user.mobile_verified
        attrs['email'] = user.email
        request = self.context.get('request')
        attrs['user_id'] = user.id
        return attrs


class ForgetPasswordSerializer(serializers.Serializer):
    country_code = serializers.CharField(error_messages={'required': "country code can't be blank"})
    mobile_number = serializers.CharField(
        error_messages={'required': "mobile_number key is required", 'blank': "mobile_number key can't be blank"})
    email = serializers.EmailField(read_only=True)
    authorization = serializers.CharField(read_only=True)
    otp = serializers.CharField(read_only=True)
    def create(self, validated_data):
        mobile_number = validated_data['mobile_number']
        if not mobile_number.isdigit():
            if len(mobile_number.split('@')) < 2:
                raise APIException400({"message": "Invalid email"})
            email = mobile_number
            try:
                user = User.objects.get(email=mobile_number)
            except:
                raise APIException400({"message": "Email doesn't exist. Please register first"})
            code = generateOTP()
            current_time = make_aware(datetime.now())
            expire_time = current_time + timedelta(minutes=30)
            otp_created = OTPStorage.objects.create(otp=code, user=user, created=expire_time)
            otp_created.save()
            from_email = settings.FROM_EMAIL
            recipient_email = mobile_number
            subject = 'OTP verification mail'
            message = 'Your One Time Password For Verification is : {}'.format(code)
            try:
                status = send_email_task.delay(subject, message, from_email, [recipient_email, ], fail_silently=False)
            except Exception as e:
                raise APIException400({"message": e, 'success': 'False'})
        else:
            if 'country_code' not in validated_data:
                raise APIException400({"message": "country code is required"})
            email = None
            country_code = validated_data['country_code']
            if not country_code.split('+')[1].isdigit():
                raise APIException400({"message": "Invalid Country Code"})
            try:
                user = User.objects.get(mobile_number=mobile_number, country_code=validated_data['country_code'])
            except:
                raise APIException400({"message": "Mobile Number doesn't exist. Please register first"})
            code = generateOTP()
            current_time = make_aware(datetime.now())
            expire_time = current_time + timedelta(minutes=30)
            timestamp = int(expire_time.strftime('%s'))
            otp_created = OTPStorage.objects.create(otp=code, user=user, created=expire_time)
            otp_created.save()
            subject = 'OTP verification'
            message = 'Your One Time Password For Verification is : {}'.format(code)
            formatted_mobile = '{}{}'.format(country_code, mobile_number)
            client = Client(account_sid, auth_token)
            try:
                message = send_mobile_task.delay(body=message, from_='+17058056223', to=formatted_mobile)
            except Exception as e:
                raise APIException400({"message": e, 'success': 'False'})
        payload = jwt_payload_handler(user)
        token = 'JWT ' + jwt_encode_handler(payload)
        validated_data['authorization'] = token
        validated_data['mobile_verified'] = user.mobile_verified
        validated_data['user_id']=user.id
        validated_data['otp']=code
        return validated_data


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        error_messages={'required': ' new_password key is required', 'blank': 'new password is required'})
    confirm_password = serializers.CharField(
        error_messages={'required': ' confirm_password key is required', 'blank': 'confirm password is required'})

    def validate_new_password(self, new_password):
        if len(new_password) < 8:
            raise APIException400({'message': 'Password must be at least 8 characters long', 'success': "False"})
        return new_password
    def validate_confirm_password(self, confirm_password):
        if len(confirm_password) < 8:
            raise APIException400({'message': 'Password must be at least 8 characters long', 'success': "False"})
        return confirm_password

class UserProfileEditSerializer(ModelSerializer):
    name = CharField(allow_blank=True)
    bio = CharField(allow_blank=True)
    location = CharField(allow_blank=True)
    website_link = CharField(allow_blank=True)
    gender = CharField(allow_blank=True)
    class Meta:
        model = UserProfile
        fields= ['name','bio','location','website_link','gender']

    def validate(self,data):
        gender = data['gender']
        if not (data['gender'] or data['name'] or data['bio'] or data['location'] or data['website_link'] or data['gender']):
            raise APIException400({"message":"update required one of these fields","status": "False"})
        if gender:  
            if not gender in ['male','female','other']:
                raise APIException400({"message":"Please provide valid gender type","status": "False"})
        return data
    def update(self, instance, validated_data):
        if not (validated_data['name'] == "" or validated_data['name'] is None):
            instance.name = validated_data.get('name', instance.name)
        if not (validated_data['bio'] == "" or validated_data['bio'] is None):
            instance.bio = validated_data.get('bio', instance.bio)
        if not (validated_data['location'] == "" or validated_data['location'] is None):
            instance.location = validated_data.get('location', instance.location)
        if not (validated_data['website_link'] == "" or validated_data['website_link'] is None):
            instance.website_link = validated_data.get('website_link', instance.website_link)
        if not (validated_data['gender'] == "" or validated_data['gender'] is None):
            instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSerializer(ModelSerializer):
    userprofile = SerializerMethodField()
    # question = SerializerMethodField()
    # comment = SerializerMethodField()
    # total_question_count = SerializerMethodField()
    # total_comment_count = SerializerMethodField()
    def get_userprofile(self,instance):
        qs = UserProfile.objects.filter(user__id=instance.id)
        data = UserProfileSerializer(qs,many=True).data
        return data
    # def get_question(self,instance):
    #     qs = Post.objects.filter(created_by__id=instance.id)
    #     data = PostListSerializer(qs,many=True).data
    #     return data
    # def get_comment(self,instance):
    #     qs = Comment.objects.filter(created_by__id=instance.id)
    #     data = CommentListSerializer(qs,many=True).data
    #     return data
    # def get_total_question_count(self, instance):
    #     qs = Post.objects.filter(created_by__id=instance.id).count()
    #     return qs
    # def get_total_comment_count(self, instance):
    #     qs = Comment.objects.filter(created_by__id=instance.id).count()
    #     return qs
    class Meta:
        model = User
        fields = ['id','email','date_joined', 'mobile_number', 'username','userprofile', 
                #'comment', #'question',
                # 'total_question_count', 'total_comment_count'
                ]


