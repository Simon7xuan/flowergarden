from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from apps.users.forms import LoginForm, RegisterPostForm, UploadImageForm, UserInfoForm, ChangePwdForm
from apps.users.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.operation.models import UserCourse, UserFavorite, UserMessage, Banner
from apps.courses.models import Course
from apps.teachers.models import Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

def message_nums(request):
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}


class MyMessageView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        current_page = "mymessage"
        for message in messages:
            message.has_read = True
            message.save()

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, per_page=6, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "messages": messages,
            "current_page": current_page
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavteacher"
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_teacher in fav_teachers:
            try:
                teacher = Teacher.objects.get(id=fav_teacher.fav_id)
                teacher_list.append(teacher)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
            "current_page": current_page
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavcourse"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
            "current_page": current_page
        })


class MyCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "mycourse"
        my_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "my_courses": my_courses,
            "current_page": current_page
        })


class ChangePwdView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return JsonResponse({
                    "status": "fail",
                    "msg": "密码不一致"
                })
            user = request.user
            user.set_password(pwd1)
            user.save()
            login(request, user)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(pwd_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    login_url = "/login/"

    # def save_file(self, file):
    #     with open("F:/pythonweb/FlowerGarden/media/head_image/uploaded.jpg", "wb") as f:
    #         for chunk in file.chunks():
    #             f.write(chunk)

    def post(self, request, *args, **kwargs):
        # 处理用户上传头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })

        # files = request.FILES["image"]
        # self.save_file(files)
        # pass


class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "info"
        return render(request, "usercenter-info.html", {
            "current_page": current_page
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(user_info_form.errors)



class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "register.html")

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            username = register_post_form.cleaned_data["username"]
            password = register_post_form.cleaned_data["password"]
            # 新建一个用户
            user = UserProfile(username=username)
            user.set_password(password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "register.html", {
                "register_post_form": register_post_form,
            })


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):

    def get(self, request, *args, **kwargs):
        # 判断用户已经登录
        if request.user.is_authenticated:
            # 重定向到主页
            return HttpResponseRedirect(reverse("index"))

        banners = Banner.objects.all()[:3]
        next = request.GET.get("next", "")
        return render(request, "login.html", {
            "next": next,
            "banners": banners
        })

    def post(self, request, *args, **kwargs):
        # 表单验证
        login_form = LoginForm(request.POST)
        banners = Banner.objects.all()[:3]
        if login_form.is_valid():
            # user_name = request.POST.get("username", "")
            # password = request.POST.get("password", "")

            # if not user_name:
            #     return render(request, "login.html", {"msg": "请输入用户名"})
            # if not password:
            #     return render(request, "login.html", {"msg": "请输入密码"})
            # if len(password) < 3:
            #     return render(request, "login.html", {"msg": "密码格式不正确"})
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)
            if user is not None:
                # 查询到用户
                login(request, user)
                # 登陆成功后返回页面
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                # 未查询到用户

                return render(request, "login.html", {
                    "msg": "用户名或密码错误",
                    "login_form": login_form,
                    "banners": banners,
                })
        else:
            return render(request, "login.html", {
                "login_form": login_form,
                "banners": banners
            })