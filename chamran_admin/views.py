from django.shortcuts import render ,HttpResponseRedirect ,reverse ,get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.core.mail import send_mail

from django.conf import settings

from . import models
from . import forms
from researcher.models import ResearcherUser ,ResearcherStatus
from expert.models import ExpertUser
from industry.models import IndustryUser

LOCAL_URL ='127.0.0.1:8000'

class Home(generic.TemplateView):
    template_name = "base.html"

# class SignupEmail(generic.FormView):
#     form_class = forms.RegisterEmailForm
#     template_name = "registration/signup.html"
#     seccess = '/'

#     def post(self, request, *args, **kwargs):
#         form = forms.RegisterEmailForm(request.POST)
#         if form.is_valid():
#             email  = form.cleaned_data['email']
#             account_type = form.cleaned_data['account_type']
#             temp_user = models.TempUser(email=email ,account_type=account_type)
            
#             subject = 'Welcome to Chamran Team!!!'

#             unique_url = LOCAL_URL + '/signup/' + temp_user.account_type + '/' + str(temp_user.unique)
#             mess = 'EmailValidation\nyour url:\n' + unique_url

#             send_mail(
#                 subject,
#                 mess,
#                 settings.EMAIL_HOST_USER,
#                 [temp_user.email ,settings.EMAIL_HOST_USER]
#             )
#             temp_user.save()
#             return HttpResponseRedirect(reverse('chamran:home'))
#         return super().post(request ,*args, **kwargs)

class SignupUser(generic.FormView):
    form_class = forms.RegisterUserForm
    template_name = 'registration/user_pass.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        temp_user = get_object_or_404(models.TempUser ,unique=code)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = forms.RegisterUserForm(request.POST)
        code = kwargs['code']
        temp_user = get_object_or_404(models.TempUser ,unique=code)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = temp_user.email
            account_type = temp_user.account_type
            user = User(username=username ,email=email)
            user.set_password(password)
            if account_type == 'researcher':
                user.save()
                researcher = ResearcherUser(user=user)
                researcher.save()
                status = ResearcherStatus(researcher_user=researcher ,status='signed_up')
                status.save()
                temp_user.delete()
                return researcher.get_absolute_url()
            elif account_type == 'expert':
                user.save()
                expert = ExpertUser(user=user)
                expert.save()
                temp_user.delete()
                return expert.get_absolute_url()

            elif account_type == 'industry':
                user.save()
                industry = IndustryUser(user=user )
                industry.save()
                temp_user.delete()
                return industry.get_absolute_url()

            return HttpResponseRedirect(reverse('chamran:home'))
        return super().post(request, *args, **kwargs)

class LoginView(generic.FormView):
    template_name = 'registration/login.html'
    form_class = forms.LoginForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        else:
            try:
                return request.user.expertuser.get_absolute_url()
            except:
                try:
                    return request.user.industryuser.get_absolute_url()
                except:
                    try:
                        return request.user.researcheruser.get_absolute_url()
                    except: 
                        return HttpResponseRedirect(reverse('chamran:home'))

    def post(self, request, *args, **kwargs):    
        if request.POST['submit'] == 'login':
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']                
                entry_user = authenticate(request ,username=username ,password=password)
                if entry_user is not None:
                    login(request ,entry_user)
                    try :
                        user = ResearcherUser.objects.get(user=entry_user)
                        return user.get_absolute_url()
                    except:
                        try:
                            user = ExpertUser.objects.get(user=entry_user)                
                            return user.get_absolute_url()
                        except:
                            try:
                                user = IndustryUser.objects.get(user=entry_user)
                                return user.get_absolute_url()
                            except:
                                return HttpResponseRedirect(reverse('chamran:home'))
                else:
                    next_form = forms.LoginForm()
                    context = {
                        'error' : 'نام کاربری یا رمز شما اشتباه است',
                        'form'  : next_form
                        }
                    return render(request ,self.template_name ,context)
        else:
            form = forms.RegisterEmailForm(request.POST)
            if form.is_valid():
                email  = form.cleaned_data['email']
                account_type = form.cleaned_data['account_type']
                temp_user = models.TempUser(email=email ,account_type=account_type)
                
                subject = 'Welcome to Chamran Team!!!'

                unique_url = LOCAL_URL + '/signup/' + temp_user.account_type + '/' + str(temp_user.unique)
                mess = 'EmailValidation\nyour url:\n' + unique_url

                send_mail(
                    subject,
                    mess,
                    settings.EMAIL_HOST_USER,
                    [temp_user.email ,settings.EMAIL_HOST_USER]
                )
                temp_user.save()
                return HttpResponseRedirect(reverse('chamran:home'))
            return super().post(request ,*args, **kwargs)
        return super().post(request ,*args, **kwargs)


class LogoutView(generic.TemplateView):
    template_name = 'registration/base.html'

    def get(self ,request ,*args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect(reverse('chamran:login'))
        return HttpResponseRedirect(reverse("chamran:home"))

def find_user(email):
    try:
        user = get_object_or_404(ExpertUser ,user__email=email)
        return 'expert'
    except:
        try:
            user = get_object_or_404(IndustryUser ,user__email=email)
            return 'industry'
        except:
            try:
                user = get_object_or_404(ResearcherUser ,user__email=email)
                return 'researcher'
            except:
                return 'None'
    return 'None'

class ResetPassword(generic.TemplateView):
    template_name = 'registration/reset_password.html'

    def post(self ,request ,*args, **kwargs):
        email = request.POST['email']
        try:
            temp_user = models.TempUser.objects.get(email=email)
        except:
            result = find_user(email)
            if result == 'None':
                return HttpResponseRedirect(reverse('chamran:home'))
            account_type = result
            temp_user = models.TempUser(email=email ,account_type=account_type)
            temp_user.save()

        subject = 'Reset your password of Chamran Team account.'

        reset_url = LOCAL_URL + '/resetpassword/' + str(temp_user.unique)
        mess = 'Reset Validation\nyour url:\n' + reset_url

        send_mail(
            subject,
            mess,
            settings.EMAIL_HOST_USER,
            [temp_user.email ,settings.EMAIL_HOST_USER]
        )

        return render(request ,'registration/password_reset_done.html' ,{})

class ResetPasswordConfirm(generic.FormView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = forms.ResetPasswordForm

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        temp_user = get_object_or_404(models.TempUser ,unique=code)
        return super().get(request, *args, **kwargs)
    
    def post(self ,request ,*args, **kwargs):
        code = kwargs['code']
        temp_user = get_object_or_404(models.TempUser ,unique=code)
        form = forms.ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = User.objects.get(email=temp_user.email)
            user.set_password(password)
            user.save()
            account_type = temp_user.account_type
            temp_user.delete()
            if account_type == 'expert':
                return user.expertuser.get_absolute_url()
            elif account_type == 'industry':
                return user.industryuser.get_absolute_url()
            elif account_type == 'researcher':
                return user.researcheruser.get_absolute_url()
        return super().post(request ,*args, **kwargs)
