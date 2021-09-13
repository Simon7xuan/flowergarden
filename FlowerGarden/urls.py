"""FlowerGarden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
import xadmin

from apps.operation.views import IndexView
from apps.users.views import LoginView, LogoutView, RegisterView
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    # 配置上传文件的访问url
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # 课程相关页面
    url(r'^course/', include(('apps.courses.urls', "courses"), namespace="course")),
    # 用户相关操作
    url(r'^op/', include(('apps.operation.urls', "operation"), namespace="op")),
    # 教师相关页面
    url(r'^teacher/', include(('apps.teachers.urls', "teachers"), namespace="teacher")),
    # 用户个人中心
    url(r'^users/', include(('apps.users.urls', "users"), namespace="users")),
    # 配置富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]

# CBV(class base view) FBV(fucntion base view)

