from django.conf.urls import url
from apps.users.views import UserInfoView, UploadImageView, ChangePwdView, MyCourseView, MyFavCourseView, MyFavTeacherView, MyMessageView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="info"),
    url(r'^image/upload/$', UploadImageView.as_view(), name="image"),
    url(r'^update/pwd/$', ChangePwdView.as_view(), name="update_pwd"),
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    url(r'^myfavteacher/$', MyFavTeacherView.as_view(), name="myfavteacher"),
    url(r'^myfavcourse/$', MyFavCourseView.as_view(), name="myfavcourse"),
    url(r'^messages/$', MyMessageView.as_view(), name="messages"),
]