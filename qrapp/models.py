from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Primary Models Initialization.


# User Profiles
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('User Name'), unique=True, max_length=250)
    fullname = models.CharField(_('Full Name'), default="", max_length=250)
    department = models.CharField(_('Department'), default="", max_length=250)
    level = models.CharField(_('Level'), default="", max_length=250)
    matric_no = models.CharField(_('Matric No'), default="", max_length=250)
    account_type = models.CharField(_('Type'), default="student", max_length=250)

    class Meta:
        db_table = 'Profile'


# Course
class Course(models.Model):
    course_name = models.CharField(_('Course Name'), default="", max_length=250)
    course_code = models.CharField(_('Course Code'), default="", max_length=250)
    course_unit = models.CharField(_('Course Unit'), default="", max_length=250)
    course_lecturer = models.ForeignKey('CustomUser', on_delete=models.CASCADE, default=1)


# Attendance
class Attendance(models.Model):
    qrcode_id = models.CharField(_('QR Code Id'), default="", max_length=250)
    student = models.ForeignKey('CustomUser', on_delete=models.CASCADE, default=1)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, default=1)


# Attendance
class ResetPassword(models.Model):
    reset_id = models.CharField(_('Reset Id'), default="", max_length=250)
    profile = models.ForeignKey('CustomUser', on_delete=models.CASCADE, default=1)


# QrCode
class QrCode(models.Model):
    qrcode = models.ImageField(upload_to='qrcode/', null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, default=1)


class ForeImage(models.Model):
    image = models.ImageField(upload_to='dumps/', null=True, blank=True)
