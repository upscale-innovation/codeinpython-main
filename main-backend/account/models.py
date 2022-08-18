
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
USER_ROLE = (('manager', 'manager'), ('worker', 'worker'), ('admin', 'admin'))
GENDER = (('male', 'male'), ('female', 'female'), ('other', 'other'))

class User(AbstractUser):
    # common fields
    email = models.EmailField(unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    country_code = models.CharField(max_length=4, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    added_by_admin = models.BooleanField(default=False)
    user_role = models.CharField(max_length=10, choices=USER_ROLE, default='worker', blank=True, null=True)


    def __str__(self):
        return str(self.pk) + '-' + str(self.username)



class OTPStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_otp')
    otp = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_used = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=False)


class UserProfile(models.Model):
    name = models.CharField(blank=True, null=True, max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    bio = models.TextField(max_length=300, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    website_link = models.TextField(max_length=100, blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profile_pic',default='default.jpg')
    gender = models.CharField(max_length=6, choices=GENDER, blank=True, null=True)

    def __str__(self):
        return str(self.pk) + '-' + str(self.user.username)