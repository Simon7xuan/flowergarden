from django.shortcuts import render
from django.views import View
from apps.teachers.models import Teacher
from pure_pagination import Paginator, PageNotAnInteger
from apps.operation.models import UserFavorite
from django.db.models import Q


def search_type(request):
        return {'s_type': "teacher"}


class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher_id):
                teacher_fav = True
        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "teacher_fav": teacher_fav,
        })


class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()

        # 教师排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        # 搜索关键词
        keywords = request.GET.get("keywords", "")
        s_type = "teacher"
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords))

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, per_page=2, request=request)
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "teachers": teachers,
            "teacher_nums": teacher_nums,
            "sort": sort,
            "keywords": keywords,
            "s_type": s_type
        })
