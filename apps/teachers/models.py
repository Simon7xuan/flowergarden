from django.db import models
from apps.users.models import BaseModel
from apps.users.models import UserProfile


class Teacher(BaseModel):
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="用户")
    name = models.CharField(max_length=50, verbose_name="教师名")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")

    class Meta:
        verbose_name = "授课教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name