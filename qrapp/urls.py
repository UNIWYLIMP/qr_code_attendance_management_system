from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='landing'),
    path('login', views.login, name='login'),
    path('authenticate_login', views.login_authenticate, name='authenticate_login'),
    path('staff_register', views.staff_register, name='staff_register'),
    path('student_register', views.student_register, name='student_register'),
    path('authenticate_student', views.authenticate_student, name='authenticate_student'),
    path('authenticate_staff', views.authenticate_staff, name='authenticate_staff'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('staff_dashboard', views.staff_dashboard, name='staff_dashboard'),
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('add_course', views.add_course, name='add_course'),
    path('delete_course/<str:course_id>', views.delete_course, name='delete_course'),
    path('explore_course/<str:course_id>', views.explore_course, name='explore_course'),
    path('otp', views.otp, name='otp'),
    path('scan_qr', views.scan_qr, name='scan_qr'),
    path('create_qr/<str:course_id>', views.create_qr, name='create_qr'),
    path('set_new_password/<str:unique_id>', views.set_new_password, name='set_new_password'),
    path('set_password', views.set_password, name='set_password'),
    path('sent_reset', views.sent_reset, name='sent_reset'),
    path('change_password', views.change_password, name='change_password'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('logout', views.logout, name='logout'),

]
