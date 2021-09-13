import re

from django import forms
from apps.operation.models import UserFavorite, CourseComments


class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]


class CommentsForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ["course", "comments"]
