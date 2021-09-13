from django.conf.urls import url
from django.urls import path

from apps.teachers.views import TeacherListView, TeacherDetailView


urlpatterns = [
    url(r'^teachers/$', TeacherListView.as_view(), name="teachers"),
    url(r'^teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]