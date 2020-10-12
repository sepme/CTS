from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget

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
    account_type = forms.CharField(max_length=10, required=True,error_messages={'required': 'لطفانوع حساب کاربری خود را مشخص کنید',})
    captcha = CaptchaField( error_messages={'required': 'لطفا کد امنیتی را وارد کنید.',
                                            'invalid' : 'کد امنیتی وارد شده نامعتبر است.'})
    #
    # class Meta:
    #     widgets = {
    #         'account_type': forms.RadioSelect(),
    #     }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        temp_user = models.TempUser.objects.filter(email=email).count()
        user = User.objects.filter(username=email).count()
        if user or temp_user:
            raise ValidationError(_('کاربر با این ایمیل ثبت نام شده است.'))

        return email


class RegisterUserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,
                               error_messages={'required': 'لطفا گذرواژه خود را وارد کنید'})
    confirm_password = forms.CharField(widget=forms.PasswordInput,
                                       error_messages={'required': "لطفا گذرواژه را دوباره وارد کنید"}
                                       )

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
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
        researcher = ResearcherUser.objects.filter(user__username=username)
        expert = ExpertUser.objects.filter(user__username=username)
        industry = IndustryUser.objects.filter(user__username=username)
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


class RecoverPasswordForm(forms.Form):
    username = forms.CharField(label='نام کاربری', error_messages={'required': 'لطفا نام کاربری خود را وارد کنید'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if not user:
            raise forms.ValidationError('کاربر با این نام کاربری ثبت نام نشده است.')
        return username

class NewsForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields = ['title', 'text', 'attachment', 'link', 'writer'] 

class ContactForm(forms.ModelForm):
    # fullname = forms.CharField(label="نام و نام خانوادگی", max_length=150, required=True, error_messages={'required': 'لطفا نام و نام خانوادگی خود را وارد کنید.',})
    # email = forms.EmailField(label="ایمیل", required=True, error_messages={'required': 'لطفا ایمیل خود را وارد کنید.',})
    # context = forms.CharField(label="پیام", max_length=1000, widget=forms.Textarea(), required=True ,error_messages={'required': 'لطفا پیام خود را وارد کنید.',})

    class Meta:
        model = models.ContactUs
        exclude = []
        error_messages = {
            'fullname' : {'required': 'لطفا نام و نام خانوادگی خود را وارد کنید.',},
            'email'    : {'required': 'لطفا ایمیل خود را وارد کنید.',},
            'context'  : {'required': 'لطفا پیام خود را وارد کنید.',}
            }
    

class FeedBackForm(forms.ModelForm):
    # captcha = CaptchaField( error_messages={'required': 'لطفا کد امنیتی را وارد کنید.',
    #                                         'invalid' : 'کد امنیتی وارد شده نامعتبر است.'})
    
    class Meta:
        model = models.FeedBack
        fields = ['email', 'opinion']
        widgets = {
            'opinion': forms.Textarea(),
        }

class CardForm(forms.ModelForm):
    deadline = forms.CharField(max_length=32, required=False)
    class Meta:
        model = models.Card
        fields = ['title',]

    def clean_title(self):
        data = self.cleaned_data["title"]
        if data == "":
            raise ValidationError("عنوان نمی تواند خالی باشد.")
        return data
    
    def clean_deadline(self):
        data = self.cleaned_data["deadline"]
        if data == "":
            raise ValidationError("زمان پایان نمی تواند خالی باشد.")
        return data
    
    
