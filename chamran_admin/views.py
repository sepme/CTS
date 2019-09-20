from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, HttpResponse, Http404, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings

from . import models
from . import forms
from researcher.models import ResearcherUser, Status
from expert.models import ExpertUser
from industry.models import IndustryUser
from django.urls import resolve

LOCAL_URL = '127.0.0.1:8000'


def find_account_type(user):
    expert = ExpertUser.objects.filter(user=user)
    researcher = ResearcherUser.objects.filter(user=user)
    industry = IndustryUser.objects.filter(user=user)
    if expert.exists():
        return 'expert'
    elif researcher.exists():
        return 'researcher'
    elif industry.exists():
        return 'industry'
    else:
        return False


class Home(generic.TemplateView):
    template_name = "base.html"


class SignupEmail(generic.FormView):
    form_class = forms.RegisterEmailForm
    template_name = "registration/signup.html"

    def post(self, request, *args, **kwargs):
        form = forms.RegisterEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            account_type = form.cleaned_data['account_type']
            temp_user = models.TempUser.objects.create(email=email, account_type=account_type)
            print(temp_user)
            subject = 'Welcome to Chamran Team!!!'

            unique_url = LOCAL_URL + '/signup/' + temp_user.account_type + '/' + str(temp_user.unique)
            message = 'EmailValidation\nyour url:\n' + unique_url

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )
            return HttpResponseRedirect(reverse('chamran:home'))
        return super().post(request, *args, **kwargs)


class SignupUser(generic.FormView):
    form_class = forms.RegisterUserForm
    template_name = 'registration/user_pass.html'

    def get(self, request, *args, **kwargs):
        path = request.path
        [account_type, uuid] = path.split('/')[2:]
        try:
            self.temp_user = models.TempUser.objects.get(account_type=account_type, unique=uuid)
        except models.TempUser.DoesNotExist:
            raise Http404('لینک مورد نظر اشتباه است (منسوخ شده است.)')
        # context = {'form': forms.RegisterUserForm(),
        #            'username': temp_user.email}
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.RegisterUserForm()
        context['username'] = self.temp_user.email
        return context

    def post(self, request, *args, **kwargs):
        form = forms.RegisterUserForm(request.POST or None)
        unique_id = kwargs['unique_id']
        print(unique_id)
        temp_user = get_object_or_404(models.TempUser, unique=unique_id)
        context = {'form': form,
                   'username': temp_user.email}
        if form.is_valid():
            password = form.cleaned_data['password']
            email = temp_user.email
            username = email
            account_type = temp_user.account_type
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            if account_type == 'researcher':
                researcher = ResearcherUser.objects.create(user=user)
                Status.objects.create(researcher_user=researcher)
                temp_user.delete()
                new_user = authenticate(request, username=username, password=password)
                if new_user is not None:
                    login(request, new_user)
                return researcher.get_absolute_url()

            elif account_type == 'expert':
                expert = ExpertUser.objects.create(user=user)
                temp_user.delete()
                new_user = authenticate(request, username=username, password=password)
                if new_user is not None:
                    login(request, new_user)
                return expert.get_absolute_url()

            elif account_type == 'industry':
                industry = IndustryUser.objects.create(user=user)
                temp_user.delete()
                new_user = authenticate(request, username=username, password=password)
                if new_user is not None:
                    login(request, new_user)
                return industry.get_absolute_url()

        return render(request, self.template_name, context)


class LoginView(generic.TemplateView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        login_form = forms.LoginForm()
        register_form = forms.RegisterEmailForm()
        context = {'form': login_form,
                   'register_form': register_form}
        if request.user.is_authenticated:
            if find_account_type(request.user) == 'expert':
                return request.user.expertuser.get_absolute_url()
            elif find_account_type(request.user) == 'researcher':
                return request.user.researcheruser.get_absolute_url()
            elif find_account_type(request.user) == 'industry':
                return request.user.industryuser.get_absolute_url()

        else:
            login_form = forms.LoginForm()
            register_form = forms.RegisterEmailForm()
            context = {'form': login_form,
                       'register_form': register_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        login_form = forms.LoginForm(request.POST or None)
        # register_form = forms.RegisterEmailForm(request.POST or None)
        context = {'form': login_form}
        # print('sign_in', 'sign_in' in request.POST)
        # print('sign_up', 'sign_up' in request.POST)
        if 'sign_in' in request.POST:
            print('sign_in')
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                entry_user = authenticate(request, username=username, password=password)
                print(entry_user)
                if entry_user is not None:
                    login(request, entry_user)

                    try:
                        user = ResearcherUser.objects.get(user=entry_user)
                        return user.get_absolute_url()
                    except ResearcherUser.DoesNotExist:
                        try:
                            user = ExpertUser.objects.get(user=entry_user)
                            return user.get_absolute_url()
                        except ExpertUser.DoesNotExist:
                            try:
                                user = IndustryUser.objects.get(user=entry_user)
                                return user.get_absolute_url()
                            except IndustryUser.DoesNotExist:
                                raise ValidationError('کابر مربوطه وجود ندارد.')
                else:
                    context = {'form': login_form,
                               'error': 'گذرواژه اشتباه است'}
        # elif 'sign_up' in request.POST:
        #     print('sign_up')
        #     if register_form.is_valid():
        #         print(register_form.cleaned_data)
        #         email = register_form.cleaned_data['email']
        #         account_type = register_form.cleaned_data['account_type']
        #         # temp_user = models.TempUser.objects.create(email=email, account_type=account_type)
        #         temp_user = models.TempUser(email=email, account_type=account_type)
        #         print(temp_user)
        #         subject = 'Welcome to Chamran Team!!!'
        #
        #         unique_url = LOCAL_URL + '/signup/' + temp_user.account_type + '/' + str(temp_user.unique)
        #         message = 'EmailValidation\nyour url:\n' + unique_url
        #         try:
        #             send_mail(
        #                 subject=subject,
        #                 message=message,
        #                 from_email=settings.EMAIL_HOST_USER,
        #                 recipient_list=[email],
        #                 fail_silently=False
        #             )
        #             temp_user.save()
        #         except TimeoutError:
        #             return HttpResponse('Timeout Error!!')
        #
        #         return HttpResponseRedirect(reverse('chamran:home'))
        return render(request, self.template_name, context)


class LogoutView(generic.TemplateView):
    template_name = 'registration/base.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse("chamran:home"))


def find_user(email):
    try:
        user = get_object_or_404(ExpertUser, user__email=email)
        return 'expert'
    except:
        try:
            user = get_object_or_404(IndustryUser, user__email=email)
            return 'industry'
        except:
            try:
                user = get_object_or_404(ResearcherUser, user__email=email)
                return 'researcher'
            except:
                return 'None'
    return 'None'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ResetPassword(generic.TemplateView):
    template_name = 'registration/reset_password.html'

    def get(self, request, *args, **kwargs):
        if find_account_type(request.user):
            if find_account_type(request.user) == 'expert':
                unique = request.user.expertuser.unique
            elif find_account_type(request.user) == 'researcher':
                unique = request.user.researcheruser.unique
            elif find_account_type(request.user) == 'industry':
                unique = request.user.industryuser.unique
            url = LOCAL_URL + '/resetpassword/' + str(unique)
            message = ':لینک تغییر رمز عبور' + '\n' + url
            send_mail(
                subject='تغییر رمز عبور',
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.username],
                fail_silently=False
            )
            return HttpResponseRedirect(reverse('chamran:home'))
        else:
            return redirect(reverse('chamran:login'))

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        try:
            temp_user = models.TempUser.objects.get(email=email)
        except:
            result = find_user(email)
            if result == 'None':
                return HttpResponseRedirect(reverse('chamran:home'))
            account_type = result
            temp_user = models.TempUser(email=email, account_type=account_type)
            temp_user.save()

        subject = 'Reset your password of Chamran Team account.'

        reset_url = LOCAL_URL + '/resetpassword/' + str(temp_user.unique)
        mess = 'Reset Validation\nyour url:\n' + reset_url

        send_mail(
            subject,
            mess,
            settings.EMAIL_HOST_USER,
            [temp_user.email, settings.EMAIL_HOST_USER]
        )

        return render(request, 'registration/password_reset_done.html', {})


class ResetPasswordConfirm(generic.FormView):
    template_name = 'registration/user_pass.html'
    form_class = forms.RegisterUserForm

    def get(self, request, *args, **kwargs):
        path = request.path
        uuid = path.split('/')[-2]
        print('uuid', uuid)
        try:
            self.expert_user = ExpertUser.objects.get(unique__exact=uuid)
        except ExpertUser.DoesNotExist:
            try:
                self.industry_user = IndustryUser.objects.get(unique__exact=uuid)
            except IndustryUser.DoesNotExist:
                try:
                    self.researcher_user = ResearcherUser.objects.get(unique__exact=uuid)
                except ResearcherUser.DoesNotExist:
                    raise Http404('لینک مورد نظر اشتباه است (منسوخ شده است.)')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.RegisterUserForm()
        # context['username'] = self.
        return context

    def post(self, request, *args, **kwargs):
        form = forms.RegisterUserForm(request.POST or None)
        unique_id = kwargs['unique_id']
        print(unique_id)
        # temp_user = get_object_or_404(models.TempUser, unique=unique_id)
        if find_account_type(request.user) == 'expert':
            user = request.user.expertuser
        elif find_account_type(request.user) == 'researcher':
            user = request.user.researcheruser
        elif find_account_type(request.user) == 'industry':
            user = request.user.industryuser

        context = {'form': form}
        if form.is_valid():
            print('user:', user)
            password = form.cleaned_data['password']
            user.user.set_password(password)
            user.user.save()
            print('username:', user.user.username, 'pass: ', user.user.password)
            new_user = authenticate(username=user.user.username, password=password)
            print('new_user:', new_user)
            if new_user is not None:
                login(request, new_user)
            return user.get_absolute_url()
            # if account_type == 'researcher':
            #     researcher = ResearcherUser.objects.create(user=user)
            #     Status.objects.create(researcher_user=researcher)
            #     temp_user.delete()
            #     new_user = authenticate(request, username=username, password=password)
            #     if new_user is not None:
            #         login(request, new_user)
            #     return researcher.get_absolute_url()
            #
            # elif account_type == 'expert':
            #     expert = ExpertUser.objects.create(user=user)
            #     temp_user.delete()
            #     new_user = authenticate(request, username=username, password=password)
            #     if new_user is not None:
            #         login(request, new_user)
            #     return expert.get_absolute_url()
            #
            # elif account_type == 'industry':
            #     industry = IndustryUser.objects.create(user=user)
            #     temp_user.delete()
            #     new_user = authenticate(request, username=username, password=password)
            #     if new_user is not None:
            #         login(request, new_user)
            #     return industry.get_absolute_url()

        return render(request, self.template_name, context)


class UserPass(generic.TemplateView):
    template_name = 'registration/user_pass.html'


def register_view(request):
    login_form = forms.LoginForm()
    register_form = forms.RegisterEmailForm(request.POST or None)
    if request.method == 'POST':
        if register_form.is_valid():
            print(register_form.cleaned_data)
            email = register_form.cleaned_data['email']
            account_type = register_form.cleaned_data['account_type']
            # temp_user = models.TempUser.objects.create(email=email, account_type=account_type)
            temp_user = models.TempUser(email=email, account_type=account_type)
            print(temp_user)
            subject = 'Welcome to Chamran Team!!!'

            unique_url = LOCAL_URL + '/signup/' + temp_user.account_type + '/' + str(temp_user.unique)
            message = 'EmailValidation\nyour url:\n' + unique_url
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False
                )
                temp_user.save()
            except TimeoutError:
                return HttpResponse('Timeout Error!!')

            return HttpResponseRedirect(reverse('chamran:home'))
    else:
        register_form = forms.RegisterEmailForm()
    return render(request, 'registration/login.html', {'form': login_form,
                                                       'register_form': register_form})
