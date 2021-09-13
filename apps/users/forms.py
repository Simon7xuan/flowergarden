from django import forms
from apps.users.models import UserProfile


class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)

    # def clean(self):
    #     pwd1 = self.cleaned_data["password1"]
    #     pwd2 = self.cleaned_data["password2"]
    #
    #     if pwd1 != pwd2:
    #         raise forms.ValidationError("密码不一致")
    #     return self.cleaned_data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name", "gender", "birthday", "address", "mobile"]


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class RegisterPostForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)

    def clean_username(self):
        # 验证用户名是否已注册
        username = self.data.get("username")
        users = UserProfile.objects.filter(username=username)
        if users:
            raise forms.ValidationError("该用户名已注册")
        return username