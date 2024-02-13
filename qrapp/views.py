from . import qr_encode
import random as ran
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import auth, User
from .models import *


# Create your views here.
def index(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


def login_authenticate(request):
    if request.method == 'GET':
        identity = request.GET.get('email')
        password = request.GET.get('password')
        message = ""
        print(identity)
        print(password)

        # user_con = CustomUser.objects.get(email=identity)
        # print(user_con.email)
        # print(user_con.password)
        if ".edu" and "@" and "calebuniversity" in identity:
            if CustomUser.objects.filter(email=identity).exists():
                user_con = CustomUser.objects.get(email=identity)
                if user_con.password == password:
                    user = ""
                else:
                    user = None
            else:
                user = None
            print(user)
        else:
            message = "Official Mail Only"
            return JsonResponse({"message": message})

        if user is not None:
            user_con = CustomUser.objects.get(email=identity)
            auth.login(request, user_con)
            email_id = identity
            message = "success"
            request.session['userId'] = email_id
            request.session['userStatus'] = CustomUser.objects.get(email=email_id).account_type
            message = "success"
            return JsonResponse({"message": message})

        else:
            message = "Invalid Details"
            return JsonResponse({"message": message})
    else:
        return redirect("/login")


def student_register(request):
    return render(request, "register-student.html")


def staff_register(request):
    return render(request, "register-staff.html")


def authenticate_student(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        fullname = request.GET.get('fullname')
        matric = request.GET.get('matric')
        level = request.GET.get('level')
        department = request.GET.get('department')

        if CustomUser.objects.filter(email=email).exists():
            message = "Email Already In Use."
            return JsonResponse({"message": message})

        elif fullname == "" or matric == "" or level == "" or department == "":
            message = "Fill All Details"
            return JsonResponse({"message": message})

        elif ".edu" and "@" and "calebuniversity" not in email:
            message = "Caleb Mail Only"
            return JsonResponse({"message": message})

        else:
            request.session['otp'] = ran.randint(1000, 9999)
            request.session['v1'] = email
            request.session['v2'] = fullname
            request.session['v3'] = matric
            request.session['v4'] = level
            request.session['v5'] = department
            request.session['v6'] = "student"
            message = "success"
            print()
            return JsonResponse({"message": message})
    else:
        return redirect("/")


def authenticate_staff(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        fullname = request.GET.get('fullname')
        staff_id = request.GET.get('uniqueId')
        matric = "...."
        level = "...."
        department = request.GET.get('department')

        if CustomUser.objects.filter(email=email).exists():
            message = "Email Already In Use."
            return JsonResponse({"message": message})

        elif fullname == "" or matric == "" or level == "" or department == "":
            message = "Fill All Details"
            return JsonResponse({"message": message})

        elif str(staff_id) != "76395293":
            message = "Incorrect Unique Staff ID."
            return JsonResponse({"message": message})

        elif ".edu" and "@" and "calebuniversity" not in email:
            message = "Caleb Mail Only"
            return JsonResponse({"message": message})

        else:
            request.session['otp'] = ran.randint(1000, 9999)
            request.session['v1'] = email
            request.session['v2'] = fullname
            request.session['v3'] = matric
            request.session['v4'] = level
            request.session['v5'] = department
            request.session['v6'] = "staff"

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message_s = (f"{request.session.get('otp')}. If you didn't initiate this action, do know there have been an "
                        f"attempt to make use of your email to register an account, kindly ignore.")
            send_mail("Caleb University QR Attendance Account OTP", message_s, email_from, recipient_list)

            message = "success"
            return JsonResponse({"message": message})
    else:
        return redirect("/")


def otp(request):
    if not request.session.get('otp', None):
        auth.logout(request)
        return redirect('/login')

    if request.method == 'POST':
        otp_input = request.POST['otp']
        if int(otp_input) == request.session.get('otp'):
            request.session['set_pass'] = "true"
            return redirect('/set_password')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('/otp')

    else:
        return render(request, "otp.html")


def set_password(request):
    if not request.session.get('otp', None):
        auth.logout(request)
        return redirect('/login')

    if not request.session.get('set_pass', None):
        auth.logout(request)
        return redirect('/login')

    if request.method == "POST":
        password_1 = request.POST["password1"]
        password_2 = request.POST["password2"]

        if password_1 == password_2:
            username = str(request.session.get('v2')).split(" ")[0] + str(ran.randint(0, 3784894303))
            if request.session.get('v6') == "student":
                user = CustomUser.objects.create_user(username=username, email=request.session.get('v1'),
                                                      password=password_1, fullname=request.session.get('v2'),
                                                      department=request.session.get('v5'),
                                                      matric_no=request.session.get('v3'),
                                                      level=request.session.get('v4'),
                                                      account_type=request.session.get('v6'))
                user.save()
                auth.login(request, user)
                request.session['userId'] = request.session.get('v1')
                request.session['userStatus'] = request.session.get('v6')
                return redirect("/dashboard")
            elif request.session.get('v6') == "staff":
                user = CustomUser.objects.create_user(username=username, email=request.session.get('v1'),
                                                      password=password_1, fullname=request.session.get('v2'),
                                                      department=request.session.get('v5'),
                                                      matric_no=request.session.get('v3'),
                                                      level=request.session.get('v4'),
                                                      account_type=request.session.get('v6'))
                user.save()
                auth.login(request, user)
                request.session['userId'] = request.session.get('v1')
                request.session['userStatus'] = request.session.get('v6')
                return redirect("/dashboard")
            else:
                return redirect("/login")
        else:
            return redirect("/set_password")

    else:
        return render(request, "set-password.html")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]

        if CustomUser.objects.filter(email=email).exists():
            unique = ran.randint(2783987637, 36789983767839678)
            user_con = CustomUser.objects.get(email=email)
            new_reset = ResetPassword(reset_id=str(unique), profile=user_con)
            new_reset.save()
            # send reset link

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = f"use this link to  reset your password gag.pythonanywhere.com/reset_lost_password/{unique}. If you didn't initiate this action, do know there have been an attempt to reset your account, kindly ignore."
            send_mail("Reset Your Caleb University QR Attendance Account", message, email_from, recipient_list)
        else:
            pass
        return redirect("/sent_reset")
    else:
        return render(request, "forget-password.html")


def sent_reset(request):
    return render(request, "reset-sent.html")


def set_new_password(request, unique_id):
    if request.method == "POST":
        password_1 = request.POST["password_1"]
        password_2 = request.POST["password_2"]
        if password_1 == password_2:
            reset_o = ResetPassword.objects.get(reset_id=request.session.get('reset_unique'))
            user = reset_o.profile
            user.password = password_1
            user.save()
            reset_o.delete()
            return redirect("/login")
        else:
            messages.info(request, 'Password Does Not Match')
            return redirect(f"/set_new_password/{unique_id}")
    else:
        if ResetPassword.objects.filter(reset_id=unique_id).exists():
            request.session['reset_unique'] = unique_id
            return render(request, "set-password-new.html", {"unique": unique_id})
        else:
            return redirect("/login")


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "staff":
        return redirect("/staff_dashboard")
    elif request.session.get('userStatus') == "student":
        return redirect("/student_dashboard")
    else:
        auth.logout(request)
        return redirect('/login')


def student_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "staff":
        return redirect("/staff_dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)
    list_attendance = list(Attendance.objects.filter(student=user))

    return render(request, "profile-student.html", {"fullname": user.fullname, "email": user_email,
                                                    "department": user.department, "matric": user.matric_no,
                                                    "level": user.level, "list_attendance": list_attendance,
                                                    "attendance_count": len(list_attendance)})


def scan_qr(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "staff":
        return redirect("/staff_dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)

    if request.method == "POST":
        qr_scan = request.FILES['image_background']
        new_image = ForeImage(image=qr_scan)
        new_image.save()

        # QR CODE Interpretation
        qr_generator = qr_encode.Encoder()
        output = qr_generator.decode_qr(new_image.image.url)
        if output == 4953:
            messages.info(request, 'Invalid Qr Code. Scan Failed')
            return redirect('/student_dashboard')
        if Attendance.objects.filter(qrcode_id=output, student=user).exists():
            messages.info(request, 'Scan Failed. Current Attendance Exist')
            return redirect('/student_dashboard')

        if "&&" in output:
            array_qr = output.split("&&")
            course_code, qr_id, lecturer_username = array_qr[0], output, array_qr[1]
            lecturer = CustomUser.objects.get(username=lecturer_username)
            single_course = Course.objects.get(course_code=course_code, course_lecturer=lecturer)
            single_attendance = Attendance(qrcode_id=qr_id, student=user, course=single_course)
            single_attendance.save()
            messages.info(request, 'Attendance Added')
            return redirect('/student_dashboard')

        else:
            messages.info(request, 'Invalid Qr Code. Scan Failed')
            return redirect('/student_dashboard')
    else:
        pass
    return redirect("/dashboard")


def staff_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "student":
        return redirect("/student_dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)
    list_of_course = list(Course.objects.filter(course_lecturer=user))

    return render(request, "profile-staff.html", {"fullname": user.fullname, "email": user_email,
                                                  "department": user.department, "list_of_course": list_of_course,
                                                  "courses_count": len(list_of_course)})


def add_course(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "student":
        return redirect("/student_dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)
    if request.method == "POST":
        course_name = request.POST["course_name"]
        course_code = request.POST["course_code"]
        course_unit = request.POST["course_unit"]
        if course_code == "" or course_unit == "" or course_name == "":
            messages.info(request, 'Fill All Details')
            return redirect("/add_course")
        else:
            new_course = Course(course_unit=course_unit, course_name=course_name, course_code=course_code,
                                course_lecturer=user)
            new_course.save()
            messages.info(request, 'Course Added Successfully')
            return redirect("/dashboard")

    return render(request, "create-course.html")


def delete_course(request, course_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "student":
        return redirect("/student_dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)

    single_course = Course.objects.get(id=int(course_id))
    if single_course.course_lecturer.email == user.email:
        messages.info(request, 'Deleted Successfully')
        single_course.delete()
        return redirect("/dashboard")
    else:
        auth.logout(request)
        messages.info(request, 'Session Terminated, Unauthorized Access')
        return redirect('/login')


def explore_course(request, course_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "student":
        return redirect("/student_dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)
    single_course = Course.objects.get(id=int(course_id))
    all_attendance = Attendance.objects.filter(course=single_course)

    data_student = {}
    data_count = {}
    uniques = []
    for x in all_attendance:
        if x.student.email in uniques:
            data_count[x.student.email] += 1
        else:
            uniques.append(x.student.email)
            data_student[x.student.email] = {
                "fullname": x.student.fullname,
                "level": x.student.level,
                "matric": x.student.matric_no,
                "department": x.student.department
            }

            data_count[x.student.email] = {"count": 1}

    data = []
    for x in uniques:
        data.append({"fullname": data_student[x].get("fullname"), "level": data_student[x].get("level"),
                     "matric": data_student[x].get("matric"),
                     "department": data_student[x].get("department"), "count": data_count[x].get("count")})

    if single_course.course_lecturer.email == user.email:
        return render(request, "attendance-list.html", {"attend_count": len(data), "data_list": data,
                                                        "course": single_course})

    else:
        auth.logout(request)
        messages.info(request, 'Session Terminated, Unauthorized Access')
        return redirect('/login')


def create_qr(request, course_id):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "student":
        return redirect("/student_dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)
    single_course = Course.objects.get(id=int(course_id))
    if single_course.course_lecturer.email == user.email:
        qrcode_id = single_course.course_code + "&&" + str(user.username) + "&&" + str(ran.randint(00000, 346787654543))
        qr_generator = qr_encode.Encoder()
        qr_file = qr_generator.create_qrcode(qrcode_id)
        new_qrcode = QrCode(qrcode=qr_file, course=single_course)
        new_qrcode.save()
        print(new_qrcode.qrcode.url)
        return render(request, "qrcode-display.html", {"qr_code": new_qrcode.qrcode.url, "course": single_course})

    else:
        auth.logout(request)
        messages.info(request, 'Session Terminated, Unauthorized Access')
        return redirect('/login')


def logout(request):
    auth.logout(request)
    return redirect('/login')


def change_password(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    user_email = request.session.get("userId")

    if request.method == "POST":
        password_1 = request.POST["password1"]
        password_2 = request.POST["password2"]
        if password_1 == password_2:
            user = CustomUser.objects.get(email=user_email)
            user.password = password_1
            user.save()
            return redirect("/dashboard")
        else:
            messages.info(request, 'Password Does Not Match')
            return redirect('/change_password')

    else:
        return render(request, "reset-password.html")


def error_404(request, exception):
    return render(request, "error-404.html", {"error_code": "404"})


def error_505(request, exception):
    return render(request, "error-404.html", {"error_code": "505"})


def error_500(request):
    return render(request, "error-404.html", {"error_code": "500"})
