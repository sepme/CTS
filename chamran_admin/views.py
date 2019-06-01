from django.shortcuts import render ,HttpResponseRedirect ,reverse ,get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

from django.conf import settings

from . import models
from . import forms

class Home(generic.TemplateView):
    template_name = "registration/login.html"

class Signup_email(generic.FormView):
    form_class = forms.Register_email_form
    template_name = "registration/signup.html"
    seccess = '/'

    def post(self, request, *args, **kwargs):
        form = forms.Register_email_form(request.POST)
        if form.is_valid():
            email  = form.cleaned_data['email']
            account_type = form.cleaned_data['account_type']
            temp_user = models.Temp_user(email=email ,account_type=account_type)
            
            subject = 'Welcome to Chamran Team!!!'

            unique_url = '127.0.0.1:8000/signup/' + temp_user.account_type + '/' + str(temp_user.unique)
            mess = 'EmailValidation\nyour url:\n' + unique_url

            send_mail(
                subject,
                mess,
                settings.EMAIL_HOST_USER,
                [temp_user.email ,settings.EMAIL_HOST_USER]
            )
            temp_user.save()
            return HttpResponseRedirect(reverse('chamran:home'))
        return HttpResponseRedirect(reverse('chamran:signup_email'))

class Signup_user(generic.FormView):
    form_class = forms.Register_user_form
    template_name = 'registration/signup.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        Temp_user = get_object_or_404(models.Temp_user ,unique=code)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = forms.Register_user_form(request.POST)
        if form.is_valid():            
            code = kwargs['code']
            temp_user = models.Temp_user.objects.filter(unique = code)[0]
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = temp_user.email
            account_type = temp_user.account_type
            user = User(username=username ,password=password ,email=email)
            if account_type == 'researcher':
                user = User(username=username ,password=password ,email=email)
                user.save()
                temp_user.delete()
                return HttpResponseRedirect(reverse('researcher:signup' ,args=[str(user.username),]))

            elif account_type == 'expert':
                user = User(username=username ,password=password ,email=email)
                user.save()
                temp_user.delete()
                return HttpResponseRedirect(reverse('expert:signup' ,args=[str(user.username),]))
                
            elif account_type == 'industry':
                user = User(username=username ,password=password ,email=email)
                user.save()
                temp_user.delete()
                return HttpResponseRedirect(reverse('industry:signup' ,args=[str(user.username),]))

            return HttpResponseRedirect(reverse('chamran:home'))
        return super().post(request, *args, **kwargs)


