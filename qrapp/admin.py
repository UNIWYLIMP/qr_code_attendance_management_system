from django.contrib import admin
from .models import *

models = [CustomUser, Course, Attendance, QrCode, ForeImage, ResetPassword]

# Register your models here.
admin.site.register(models)
