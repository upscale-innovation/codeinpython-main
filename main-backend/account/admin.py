from django.contrib import admin

# Register your models here.

from account.models import *

admin.site.register([User, OTPStorage, UserProfile])

