from django.shortcuts import render
from django.views.generic.base import View
from apps.courses.models import Course, CourseResource, Video
from apps.operation.models import UserFavorite, UserCourse, CourseComments, Banner
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


# def is_banner(request):
#     banners = Banner.objects.all().order_by("index")


def search_type(request):
    return {'s_type': "course"}


class VideoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, video_id, *args, **kwargs):
        # 获取课程章节信息
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        # 用户和课程的关联
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 取出课程资源
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "course_resources": course_resources,
            "video": video
        })


class CourseCommentsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": course_resources,
            "comments": comments,
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        # 获取课程章节信息
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 用户和课程的关联
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        # 取出课程资源
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "course_resources": course_resources

        })


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        # 获取课程列表信息
        all_courses = Course.objects.order_by("-add_time")

        # 热门课程推荐
        hot_courses = Course.objects.order_by("-click_nums")[:2]

        # 搜索关键词
        keywords = request.GET.get("keywords", "")
        s_type = "course"
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) |
                                             Q(tag__icontains=keywords) | Q(teacher__name__icontains=keywords))

        # 课程排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=6, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
            "keywords": keywords,
            "s_type": s_type
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        # 获取课程详情
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 获取收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav = True

        # 通过课程tag做推荐
        tag = course.tag
        related_course = []
        if tag:
            related_course = Course.objects.filter(tag=tag).exclude(id__in=[course.id])[:1]

        return render(request, "course-detail.html", {
            "course": course,
            "has_fav": has_fav,
            "related_course": related_course
        })

