import xadmin

from apps.teachers.models import Teacher


class TeacherAdmin(object):
    list_display = ["name", "points", "age", "image"]
    search_fields = ["name", "points"]
    list_filter = ["name", "points", "age", "add_time"]
    llist_editable = ["name", "points"]


xadmin.site.register(Teacher, TeacherAdmin)