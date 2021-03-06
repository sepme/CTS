import datetime

from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, HttpResponse, Http404, redirect
from django.views import generic, View
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.exceptions import ValidationError, PermissionDenied
from django.conf import settings
from django.template.loader import get_template
from django.urls import resolve
from django.contrib.contenttypes.models import ContentType

from persiantools.jdatetime import JalaliDate

from chamran_admin.models import Message
from . import models, forms
from researcher.models import ResearcherUser, Status
from expert.models import ExpertUser
from industry.models import IndustryUser, Comment

LOCAL_URL = 'chamranteambot.pythonanywhere.com'


def jalali_date(jdate):

    return str(jdate.day) + ' ' + MessagesView.jalali_months[jdate.month - 1] + ' ' + str(jdate.year)



def get_message_detail(request, message_id):
    message = Message.objects.filter(receiver=request.user).get(id=message_id)
    if not message.read_by.filter(username=request.user.username).exists():
        message.read_by.add(request.user)
    attachment = None
    if message.attachment:
        attachment = message.attachment.url[message.attachment.url.find('media', 2):]
    return JsonResponse({
        'text': message.text,
        'date': jalali_date(JalaliDate(message.date)),
        'title': message.title,
        'code': message.code,
        'type': message.type,
        'attachment': attachment,
    })


class MessagesView(LoginRequiredMixin ,generic.TemplateView ):
    template_name = '../registration/chamran_admin/messages.html'
    login_url = "/login"
    jalali_months = ('فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر',
                     'دی', 'بهمن', 'اسفند')

    @staticmethod
    def date_dif(jdate):
        delta = relativedelta(datetime.datetime.now(), jdate.to_gregorian())
        if delta.years > 0:
            return '(' + str(delta.years) + ' سال پیش' + ')'
        elif delta.months > 0:
            return '(' + str(delta.months) + ' ماه پیش' + ')'
        elif delta.days > 0:
            return '(' + str(delta.days) + ' روز پیش' + ')'
        else:
            return '(امروز)'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_messages = Message.get_user_messages(self.request.user)
        top_3 = []
        other_messages = []
        for i, message in enumerate(all_messages):
            jdate = JalaliDate(message.date)
            if i < 3:
                top_3.append((message, jalali_date(jdate), MessagesView.date_dif(jdate), message.read_by.filter(
                    username=self.request.user.username).exists()))

            other_messages.append((message, jalali_date(jdate), MessagesView.date_dif(jdate),
                                    message.read_by.filter(
                                        username=self.request.user.username).exists()))
        context['top_3'] = top_3
        context['other_messages'] = other_messages
        context['account_type'] = find_account_type(self.request.user)
        return context


def find_account_type(user):
    expert = ExpertUser.objects.filter(user=user)
    if expert.exists():
        return 'expert'
    industry = IndustryUser.objects.filter(user=user)
    if industry.exists():
        return 'industry'
    researcher = ResearcherUser.objects.filter(user=user)
    if researcher.exists():
        return 'researcher'
    else:
        return False


def find_user(user):
    if find_account_type(user) == 'expert':
        return user.expertuser
    elif find_account_type(user) == 'researcher':
        return user.researcheruser
    elif find_account_type(user) == 'industry':
        return user.industryuser
    else:
        return False


def get_user_by_unique_id(unique):
    expert = ExpertUser.objects.filter(unique__exact=unique)
    researcher = ResearcherUser.objects.filter(unique__exact=unique)
    industry = IndustryUser.objects.filter(unique__exact=unique)
    if expert.exists():
        return expert[0]
    elif researcher.exists():
        return researcher[0]
    elif industry.exists():
        return industry[0]
    else:
        return False


class Home(generic.TemplateView):
    template_name = "../registration/base.html"
    
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('chamran:login'))

class SignupEmail(generic.FormView):
    form_class = forms.RegisterEmailForm
    template_name = "registration/signup.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['register_form'] = forms.RegisterEmailForm()
    #     return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = forms.RegisterEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            account_type = form.cleaned_data['account_type']
            # temp_user = models.TempUser.objects.create(email=email, account_type=account_type)
            temp_user = models.TempUser(email=email, account_type=account_type)
            subject = 'Welcome to Chamran Team!!!'

            unique_url = LOCAL_URL + '/signup/' + temp_user.account_type + '/' + str(temp_user.unique)
            message = 'EmailValidation\nyour url:\n' + unique_url
            try:
                # send_mail(
                #     subject=subject,
                #     message=message,
                #     from_email=settings.EMAIL_HOST_USER,
                #     recipient_list=[email],
                #     fail_silently=False
                # )
                email_template = get_template('registration/email_template.html')
                msg = EmailMultiAlternatives(subject=subject, body=message, from_email=settings.EMAIL_HOST_USER,
                                             to=[email])
                msg.attach_alternative(email_template, "text/html")
                msg.send()
                temp_user.save()
            except TimeoutError:
                return HttpResponse('Timeout Error!!')

            return HttpResponseRedirect(reverse('chamran:home'))

        return super().post(request, *args, **kwargs)


def signup_email_ajax(request):
    form = forms.RegisterEmailForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        account_type = form.cleaned_data['account_type']
        # temp_user = models.TempUser.objects.create(email=email, account_type=account_type)
        temp_user = models.TempUser(email=email, account_type=account_type)
        subject = 'تکمیل ثبت نام'

        unique_url = LOCAL_URL + '/signup/' + temp_user.account_type + '/' + str(temp_user.unique)
        message = unique_url
        data = {'success': 'successful'}
        try:
            # send_mail(
            #     subject=subject,
            #     message=message,
            #     from_email=settings.EMAIL_HOST_USER,
            #     recipient_list=[email],
            #     fail_silently=False
            # )
            html_template = get_template('registration/email_template.html')
            email_template = html_template.render({'message': message, 'proper_text': 'تکمیل ثبت نام'})
            msg = EmailMultiAlternatives(subject=subject, from_email=settings.EMAIL_HOST_USER,
                                         to=[email])
            msg.attach_alternative(email_template, 'text/html')
            msg.send()
            temp_user.save()
        except TimeoutError:
            return JsonResponse({'Error': 'Timeout Error!'})
        return JsonResponse(data)
    else:
        print('form error')
        return JsonResponse(form.errors, status=400)


def login_ajax(request):
    form = forms.LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        entry_user = authenticate(request, username=username, password=password)
        data = {'success': 'successful'}
        if entry_user is not None:
            login(request, entry_user)

            try:
                user = ResearcherUser.objects.get(user=entry_user)
                data['type'] = 'researcher'
            except ResearcherUser.DoesNotExist:
                try:
                    user = ExpertUser.objects.get(user=entry_user)
                    data['type'] = 'expert'
                except ExpertUser.DoesNotExist:
                    try:
                        user = IndustryUser.objects.get(user=entry_user)
                        data['type'] = 'industry'
                    except IndustryUser.DoesNotExist:
                        raise ValidationError('کابر مربوطه وجود ندارد.')
            data['next'] = request.POST.get('next')
            return JsonResponse(data)
            # return HttpResponseRedirect(reverse)
        else:
            # context = {'form': form,
            #            'error': 'گذرواژه اشتباه است'}
            return JsonResponse({
                'password': 'گذرواژه اشتباه است'
            } ,status=400)
    else:
        print('form error')
        return JsonResponse(form.errors, status=400)

def addGroup(user, group_name):
    if not Group.objects.filter(name = group_name).exists():
        newGroup = Group(name=group_name)
        newGroup.save()
        if group_name == "Researcher":
            ctype = ContentType.objects.get_for_model(ResearcherUser)
        elif group_name == "Expert":
            ctype = ContentType.objects.get_for_model(ExpertUser)
        else:
            ctype = ContentType.objects.get_for_model(IndustryUser)
        permissionName = 'be_' + group_name.lower()
        permission = Permission.objects.get(content_type=ctype, codename=permissionName)
        newGroup.permissions.add(permission)
        newGroup.user_set.add(user)
        newGroup.save()
    else:
        group = Group.objects.get(name = group_name)
        group.user_set.add(user)
        group.save()

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
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        [account_type, uuid] = self.request.path.split('/')[2:]
        try:
            temp_user = models.TempUser.objects.get(account_type=account_type, unique=uuid)
        except models.TempUser.DoesNotExist:
            raise Http404('لینک مورد نظر اشتباه است (منسوخ شده است.)')
        context['username'] = temp_user.email
        return context

    def form_valid(self, form):
        unique_id = self.kwargs['unique_id']
        temp_user = get_object_or_404(models.TempUser, unique=unique_id)
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
            new_user = authenticate(self.request, username=username, password=password)
            if new_user is not None:
                login(self.request, new_user)
            addGroup(user, "Researcher")
            ctype = ContentType.objects.get_for_model(ResearcherUser)
            permission = Permission.objects.get(content_type=ctype, codename='is_active')
            user.user_permissions.add(permission)
            user.save()    
            return researcher.get_absolute_url()

        elif account_type == 'expert':
            expert = ExpertUser.objects.create(user=user)
            temp_user.delete()
            new_user = authenticate(self.request, username=username, password=password)
            if new_user is not None:
                login(self.request, new_user)
            addGroup(new_user, "Expert")
            return expert.get_absolute_url()

        elif account_type == 'industry':
            industry = IndustryUser.objects.create(user=user)
            temp_user.delete()
            new_user = authenticate(self.request, username=username, password=password)
            if new_user is not None:
                login(self.request, new_user)
            addGroup(new_user, "Industry")
            return industry.get_absolute_url()
        return super().form_valid(form)

class LoginView(generic.TemplateView):
    template_name = 'registration/login.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                return find_user(request.user).get_absolute_url()
        except:
            pass
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = forms.LoginForm()
        context['register_form'] = forms.RegisterEmailForm()
        if self.request.GET.get('next') :
            context['next'] = self.request.GET.get('next')
        return context
    

class LogoutView(generic.TemplateView):
    template_name = 'registration/base.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse("chamran:home"))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ResetPassword(generic.TemplateView):
    template_name = 'registration/reset_password.html'

    def get(self, request, *args, **kwargs):
        if find_account_type(request.user):
            unique = find_user(request.user).unique
            url = LOCAL_URL + '/resetpassword/' + str(unique)
            message = url
            subject = 'تغییر رمز عبور'

            try:
                html_template = get_template('registration/email_template.html')
                email_template = html_template.render({'message': message, 'proper_text': 'تغییر رمز عبور'})
                msg = EmailMultiAlternatives(subject=subject, from_email=settings.EMAIL_HOST_USER,
                                             to=[request.user.username])
                msg.attach_alternative(email_template, 'text/html')
                msg.send()
            except TimeoutError:
                return Http404('Timeout Error!')

            return HttpResponseRedirect(reverse('chamran:home'))
        else:
            return redirect(reverse('chamran:login'))


class ResetPasswordConfirm(generic.FormView):
    template_name = 'registration/user_pass.html'
    form_class = forms.RegisterUserForm

    def get(self, request, *args, **kwargs):
        path = request.path
        uuid = path.split('/')[-2]
        try:
            ExpertUser.objects.get(unique__exact=uuid)
        except ExpertUser.DoesNotExist:
            try:
                IndustryUser.objects.get(unique__exact=uuid)
            except IndustryUser.DoesNotExist:
                try:
                    ResearcherUser.objects.get(unique__exact=uuid)
                except ResearcherUser.DoesNotExist:
                    raise Http404('لینک مورد نظر اشتباه است (منسوخ شده است.)')
        return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super(ResetPasswordConfirm, self).get_context_data(**kwargs)
    #     # context['form'] = forms.RegisterUserForm()
    #     # print(self.user.user.username)
    #     print('context recover', self.recover)
    #     if self.recover:
    #         context['username'] = self.user.user.username
    #     return context

    def post(self, request, *args, **kwargs):
        # print('recover: \nuser: ', self.recover, self.user)
        form = forms.RegisterUserForm(request.POST or None)
        unique_id = kwargs['unique_id']
        user = find_user(request.user)
        # context = {'form': form,
        #            'username': self.user.user.username}
        if form.is_valid():
            password = form.cleaned_data['password']
            user.user.set_password(password)
            user.user.save()
            new_user = authenticate(username=user.user.username, password=password)
            if new_user is not None:
                login(request, new_user)
            return user.get_absolute_url()

        return super().post(request, *args, **kwargs)


class RecoverPasswordConfirm(generic.FormView):
    template_name = 'registration/user_pass.html'
    form_class = forms.RegisterUserForm

    def get(self, request, *args, **kwargs):
        path = request.path
        uuid = path.split('/')[-2]
        try:
            user = ExpertUser.objects.get(unique__exact=uuid)
        except ExpertUser.DoesNotExist:
            try:
                user = IndustryUser.objects.get(unique__exact=uuid)
            except IndustryUser.DoesNotExist:
                try:
                    user = ResearcherUser.objects.get(unique__exact=uuid)
                except ResearcherUser.DoesNotExist:
                    raise Http404('لینک مورد نظر اشتباه است (منسوخ شده است.)')
        return render(request, self.template_name, {'form': forms.RegisterUserForm(),
                                                    'username': user.user.username})

    def post(self, request, *args, **kwargs):
        # print('recover: \nuser: ', self.recover, self.user)
        form = forms.RegisterUserForm(request.POST or None)
        unique_id = kwargs['unique_id']
        user = get_user_by_unique_id(unique_id)
        context = {'form': form,
                   'username': user.user.username}
        if form.is_valid():
            password = form.cleaned_data['password']
            user.user.set_password(password)
            user.user.save()
            new_user = authenticate(username=user.user.username, password=password)
            if new_user is not None:
                login(request, new_user)
            return user.get_absolute_url()

        return render(request, self.template_name, context)


class UserPass(generic.TemplateView):
    template_name = 'registration/user_pass.html'


def notFound404(request ,exception):
    context = {'data' : exception}
    return render(request, '../registration/404Template.html', context)

def notFound500(request):
    return render(request, '../registration/404Template.html', {})

def Handler403(request ,exception):
    context = {'data' : exception}
    return render(request, '../registration/403Template.html', context)

class RecoverPassword(generic.TemplateView):
    template_name = 'registration/recover_pass.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = forms.RecoverPasswordForm
    #     return context

def RecoverPassword_ajax(request):
    form = forms.RecoverPasswordForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        temp = get_object_or_404(User, username=username)
        user = find_user(temp)
        url = LOCAL_URL + '/recover_password/' + str(user.unique)
        subject = 'بازیابی رمز عبور'
        message = url
        try:
            html_template = get_template('registration/email_template.html')
            email_template = html_template.render({'message': message, 'proper_text': 'بازیابی رمز عبور'})
            msg = EmailMultiAlternatives(subject=subject, from_email=settings.EMAIL_HOST_USER,
                                            to=[username])
            msg.attach_alternative(email_template, 'text/html')
            msg.send()            
        except TimeoutError:
            print("Timeout Occure.")
            return JsonResponse({"error" : "couldn't send email"} ,status=400)
        response = {"seccessful" :"seccessful"}
        return JsonResponse(response)
    return JsonResponse(form.errors ,status=400)

def DeleteComment(request):
    try:
        comment = get_object_or_404(Comment ,pk=request.POST['id'])
        comment.delete()
    except:
        return JsonResponse({} ,400)
    return JsonResponse({'successful' :"successful"})