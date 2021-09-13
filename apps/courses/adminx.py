import xadmin
from import_export import resources

from apps.courses.models import Course, Lesson, Video, CourseResource, BannerCourse
from xadmin.layout import Fieldset, Main, Side, Row

class GlobalSettings(object):
    site_title = "FlowerGarden"
    site_footer = "FlowerGarden"
    # menu_style = "accordion"


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]

    def queryset(self):
        # 数据过滤
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonInline(object):
    model = Lesson
    # style = "tab"
    extra = 0
    exclude = ["add_time"]


class CourseResourseInline(object):
    model = CourseResource
    style = "tab"
    extra = 1
    exclude = ["add_time"]


class MyResource(resources.ModelResource):

    class Meta:
        model = Course
        # fields = ('name', 'description',)
        # exclude = ()


class CourseAdmin(object):
    import_export_args = {'import_resource_class': MyResource, 'export_resource_class': MyResource}
    list_display = ['name', 'desc', 'go_to', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]
    readonly_fields = ["click_nums", "fav_nums", "students", "add_time"]
    ordering = ["-students"]
    model_icon = 'fa fa-address-book'
    inlines = [LessonInline, CourseResourseInline]
    style_fields = {
        "detail": "ueditor"
    }

    def queryset(self):
        # 数据过滤
        qs = super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset("讲师信息",
                             'teacher', 'course_org',
                             css_class='unsort no_title'
                             ),
                    Fieldset("基本信息",
                             'name', 'desc',
                             Row('learn_times', 'degree'),
                             Row('category', 'tag'),
                             'youneed_know', 'teacher_tell', 'detail',
                             ),
                ),
                Side(
                    Fieldset("访问信息",
                             'fav_nums', 'click_nums', 'students', 'add_time'
                             ),
                ),
                Side(
                    Fieldset("选择信息",
                             'is_banner', 'is_classics'
                             ),
                )
            )
        return super(CourseAdmin, self).get_form_layout()


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']


xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)