from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from . import models

ACCOUNT_CHOICE =(
    ('industry'   ,'Industry'),
    ('expert'     ,'Expert'),
    ('researcher' ,'Researcher'),
)

class Register_email_form(forms.Form):
    email = forms.EmailField(label="ایمیل")
    account_type = forms.ChoiceField(choices=ACCOUNT_CHOICE)
    class Meta:
        widgets = {
            'account_type': forms.RadioSelect(),
        }
    
    def clean_email(self):
        email           = self.cleaned_data["email"]
        check_tempUsers = models.Temp_user.objects.filter(email=email).count()
        check_User      = User.objects.filter(email=email).count()
        if check_tempUsers or check_User:
            raise(ValidationError(_('ایمیل وارد شده تکراری است')))
        return email

class Register_user_form(forms.Form):
    username        = forms.CharField(label="نام کاربری")
    password        = forms.CharField(widget=forms.PasswordInput ,label="رمز عبور")
    confirm_password = forms.CharField(widget=forms.PasswordInput ,label="تایید رمز عبور")
    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password' : forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        check_User      = User.objects.filter(username = username)
        
        if check_User:
            raise(ValidationError(_('نام کاربری وارد شده تکراری است')))
        return username

    def checkPassword(self):        
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            return False
        return True

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if not self.checkPassword():
            raise(ValidationError(_('رمز عبور تطابق ندارد')))
        return confirm_password