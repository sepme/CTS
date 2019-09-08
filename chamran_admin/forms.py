from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from . import models
from researcher.models import ResearcherUser
from expert.models import ExpertUser
from industry.models import IndustryUser

ACCOUNT_CHOICE = (
    ('industry', 'Industry'),
    ('expert', 'Expert'),
    ('researcher', 'Researcher'),
)


class RegisterEmailForm(forms.Form):
    email = forms.EmailField(label="ایمیل", error_messages={'required': 'لطفا ایمیل خود را وارد کنید',
                                                            'invalid': 'ایمیل وارد شده نامعتبر است'})
    account_type = forms.ChoiceField(choices=ACCOUNT_CHOICE, label='نوع حساب کاربری')

    class Meta:
        widgets = {
            'account_type': forms.RadioSelect(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        check_tempUsers = models.TempUser.objects.filter(email=email).count()
        check_User = User.objects.filter(email=email).count()
        if check_tempUsers or check_User:
            raise ValidationError(_('ایمیل وارد شده تکراری است'))

        return email


class RegisterUserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور",
                               error_messages={'required': 'لطفا گذرواژه خود را وارد کنید'})
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="تایید رمز عبور",
                                       error_messages={'required': "لطفا گذرواژه را دوباره وارد کنید"})

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        print('password: ', password, 'confirm: ', confirm_password)
        if len(password) < 8:
            raise forms.ValidationError('گذرواژه حداقل باید هشت رقم داشته باشد')
        elif password != confirm_password:
            raise forms.ValidationError('گذرواژه ها با هم مطابقت ندارند')


class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری', error_messages={'required': 'لطفا نام کاربری خود را وارد کنید'})
    password = forms.CharField(widget=forms.PasswordInput(), label='رمز عبور',
                               error_messages={'required': 'لطفا گذرواژه خود را وارد کنید'})

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        print(username)
        researcher = ResearcherUser.objects.filter(user__username=username)
        expert = ExpertUser.objects.filter(user__username=username)
        industry = IndustryUser.objects.filter(user__username=username)
        print(researcher, expert, industry)
        if not (researcher or expert or industry):
            raise forms.ValidationError('این نام کابری ثبت نام نشده است')
        return username


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label="رمز عبور")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="تایید رمز عبور")

    class Meta:
        widget = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

    def checkPassword(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            return False
        return True

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if not self.checkPassword():
            raise (ValidationError(_('رمز عبور تطابق ندارد.')))
        return confirm_password

    def clean_password(self):
        data = self.cleaned_data["password"]
        return data
