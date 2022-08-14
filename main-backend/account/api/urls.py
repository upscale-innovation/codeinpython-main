from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    #authentication
    path('signup', UserCreateAPIView.as_view(), name='signup'),
    path('login', LogInUser.as_view(), name='login'),
    path('forget_password', ForgetPasswordAPIView.as_view(), name='forget_password'),
    path('otp_resend', ResendOTPAPIView.as_view(), name='otp_resend'),
    path('otp_verify', VerifyOTP.as_view(), name='otp_verify'),
    path('reset_password', ResetPasswordResetAPIView.as_view(), name='reset_password'),
    #user profile
    path('edit_profile/', UserProfileEditAPIView.as_view(), name='edit_profile'),
    path('user_profile/', UserProfileView.as_view(), name='user_profile'),
    path('total_users/', TotalUsersView.as_view(), name='total_users'),
]



