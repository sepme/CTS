import datetime
import os

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.files.base import ContentFile
from django.forms import model_to_dict
from django.views import generic, View
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.template.loader import get_template

from persiantools.jdatetime import JalaliDate

from ChamranTeamSite import settings
from industry.models import IndustryForm, Comment
from expert import models as expert_models
from . import models, forms
from expert.models import ExpertUser
from researcher.models import Technique
from chamran_admin.models import Message


# function name says it all :)
def gregorian_to_numeric_jalali(date):
    if date:
        j_date = JalaliDate(date)
        return str(j_date.year) + '/' + str(j_date.month) + '/' + str(j_date.day)
    else:
        return "نا مشخص"


# returns the difference between the two dates. e.g. 3 ruz, 5 sal, ...
def date_dif(start_date, deadline_date):
    delta = relativedelta(deadline_date, start_date)
    if delta.years != 0:
        return str(delta.years) + ' سال'
    elif delta.months != 0:
        return str(delta.months) + ' ماه'
    elif delta.days != 0:
        return str(delta.days) + ' روز'
    else:
        return 'امروز'


# is called through an ajax request. returns the comments on a particular project with a particular expert
@permission_required('industry.be_industry', login_url='/login/')
def get_comments_with_expert(request):
    comment_list = Comment.objects.filter(project_id=request.GET.get('project_id'),
                                          industry_user=request.user.industryuser,
                                          expert_user_id=request.GET.get('expert_id'))
    json_response = {'comments': []}
    for comment in comment_list:
        json_response['comments'].append({
            'id': comment.id,
            'text': comment.description,
            'sender_type': comment.sender_type
        })


def usualShow(request, project):
    data = model_to_dict(project.project_form)
    data['deadline'] = 'نا مشخص'
    if project.status == 1 and project.date_project_started and project.date_phase_three_deadline:
        data['deadline'] = date_dif(datetime.datetime.now().date(), project.date_phase_three_deadline)
    else:
        data['deadline'] = date_dif(project.date_project_started, project.date_phase_three_deadline)
    data['submission_date'] = gregorian_to_numeric_jalali(project.date_submitted_by_industry)
    for ind, value in enumerate(data['key_words']):
        data['key_words'][ind] = value.__str__()
    data['required_technique'] = []
    evaluation_history = request.user.industryuser.expertevaluateindustry_set.filter(project=project)
    data['status'] = project.status
    data['accepted'] = False
    data['vote'] = False

    data['expert_messaged'] = []
    for expert in project.expert_messaged.all():
        data['expert_messaged'].append({
            'id': expert.id,
            'name': expert.expertform.__str__(),
            'applied': expert in project.expert_applied.all(),
        })
    for expert in project.expert_applied.all():
        if expert not in project.expert_messaged.all():
            data['expert_messaged'].append({
                'id': expert.id,
                'name': expert.expertform.__str__(),
                'applied': expert in project.expert_applied.all(),
            })
    return data


def ActiveProject(request, project, data):
    data['accepted'] = True
    data['comments'] = []
    for comment in Comment.objects.filter(project=project).exclude(industry_user=None):
        try:
            url = comment.attachment.url[comment.attachment.url.find('media', 2):]
        except:
            url = "None"
        data['comments'].append({
            'id': comment.id,
            'text': comment.description,
            'sender_type': comment.sender_type,
            'attachment': url,
            'pk': comment.pk,
        })
        if comment.sender_type == "expert" or comment.sender_type == "system":
            comment.status = "seen"
            comment.save()
    data['deadline'] = 'نا مشخص'
    data['submission_date'] = gregorian_to_numeric_jalali(project.date_submitted_by_industry)
    evaluation_history = request.user.industryuser.expertevaluateindustry_set.filter(project=project)
    data['status'] = project.status
    data['vote'] = False
    try:
        if datetime.date.today() > project.date_finished:
            if len(evaluation_history.filter(phase=3)) == 0:
                data['vote'] = True
        elif datetime.date.today() > project.date_phase_two_finished:
            if len(evaluation_history.filter(phase=2)) == 0:
                data['vote'] = True
        elif datetime.date.today() > project.date_phase_one_finished:
            if len(evaluation_history.filter(phase=1)) == 0:
                data['vote'] = True
    except:
        pass

    industryform = request.user.industryuser.profile
    projectDate = [
        gregorian_to_numeric_jalali(project.date_start),
        gregorian_to_numeric_jalali(project.date_project_started),
        gregorian_to_numeric_jalali(project.date_phase_two_deadline),
        gregorian_to_numeric_jalali(project.date_phase_three_deadline),
        gregorian_to_numeric_jalali(project.date_finished),
    ]
    data['timeScheduling'] = projectDate
    # data = {
    data["industry_name"] = industryform.name
    data["industry_logo"] = industryform.photo.url
    data['enforcer_name'] = str(project.expert_accepted.expertform)
    data['enforcer_id'] = project.expert_accepted.pk
    data["executive_info"] = project.executive_info
    data["budget_amount"] = project.project_form.required_budget
    data["techniques"] = []
    # }
    projectRequest = expert_models.ExpertRequestedProject.objects.filter(project=project).filter(
        expert=project.expert_accepted).first()
    for technique in projectRequest.required_technique.all():
        data["techniques"].append(technique.__str__())

    return data


# is called by an ajax request and returns the necessary information to display the project on the front-end
@permission_required('industry.be_industry', login_url='/login/')
def show_project_ajax(request):
    project = models.Project.objects.filter(id=request.GET.get('id')).first()
    data = usualShow(request, project)
    if project.expert_accepted:
        ActiveProject(request, project, data)
    return JsonResponse(data)


@permission_required('industry.be_industry', login_url='/login/')
def GetComment(request):
    expert_id = request.GET.get('expert_id')
    project_id = request.GET.get('project_id')
    project = get_object_or_404(models.Project, pk=project_id)
    expert = get_object_or_404(ExpertUser, pk=expert_id)
    all_comments = models.Comment.objects.filter(project=project)
    comments = all_comments.filter(expert_user=expert).exclude(industry_user=None)
    response = []
    for comment in comments:
        try:
            url = comment.attachment.url[comment.attachment.url.find('media', 2):]
        except:
            url = "None"
        temp = {
            'pk': comment.pk,
            'text': comment.description,
            'replied_text': comment.replied_text,
            'sender_type': comment.sender_type,
            'attachment': url,
        }
        response.append(temp)
        if comment.sender_type == 'expert' or comment.sender_type == 'system':
            comment.status = "seen"
            comment.save()
    if project.expert_accepted:
        if project.expert_accepted == expert:
            data = {
                'comment': response,
                'accepted': True,
                'enforcer': True
            }
        else:
            data = {
                'comment': response,
                'accepted': True,
                'enforcer': False
            }
        return JsonResponse(data=data)
    if expert in project.expert_applied.all():
        data = {
            'comment': response,
            'accepted': False,
            'applied': True
        }
    else:
        data = {
            'comment': response,
            'accepted': False,
            'applied': False
        }
    return JsonResponse(data=data)


@permission_required('industry.be_industry', login_url='/login/')
def accept_project(request):
    expert = ExpertUser.objects.filter(pk=request.POST['expert_id']).first()
    project = models.Project.objects.filter(pk=request.POST['project_id']).first()
    project.expert_accepted = expert
    project.date_start = datetime.date.today()
    project.status = 2
    project.save()
    expert.status = 'involved'
    expert.save()
    data = {'success': 'successful'}
    return JsonResponse(data=data)


@permission_required('industry.be_industry', login_url='/login/')
def refuse_expert(request):
    expert = ExpertUser.objects.filter(pk=request.POST['expert_id']).first()
    project = models.Project.objects.filter(pk=request.POST['project_id']).first()
    project.expert_banned.add(expert)
    project.save()
    data = {'success': 'successful'}
    return JsonResponse(data=data)


# this function is called when the industry user comments on a project
@permission_required('industry.be_industry', login_url='/login/')
def submit_comment(request):
    form = forms.CommentForm(request.POST, request.FILES)
    if form.is_valid():
        project = models.Project.objects.filter(id=int(request.POST['project_id'])).first()
        expert_user = get_object_or_404(ExpertUser, pk=request.POST['expert_id'])
        description = form.cleaned_data['description']
        attachment = form.cleaned_data['attachment']
        new_comment = Comment.objects.create(project=project,
                                             industry_user=request.user.industryuser,
                                             sender_type="industry",
                                             expert_user=expert_user,
                                             description=description,
                                             attachment=attachment,
                                             status='unseen')
        new_comment.save()
        if attachment is not None:
            url = new_comment.attachment.url[new_comment.attachment.url.find('media', 2):]
            data = {
                'success': 'successful',
                'attachment': url,
                'description': description,
            }
        else:
            data = {
                'success': 'successful',
                'attachment': "None",
                'description': description,
            }
        return JsonResponse(data=data)
    return JsonResponse(data=form.errors, status=400)


# main page for an industry user
class Index(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    template_name = 'industry/index.html'
    form_class = forms.basicInterfacePersonForm
    login_url = '/login/'
    success_url = '/industry'
    permission_required = ('industry.be_industry',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.industryuser.status != 'signed_up':
            industry_user = self.request.user.industryuser
            context['projects'] = models.Project.objects.filter(industry_creator=industry_user)
        else:
            context['RandD_form'] = forms.RandDBasicInfoForm
            context['researchGroup_form'] = forms.ResearchGroupBasicInfoForm
        return context

    def form_invalid(self, form):
        context = self.get_context_data()
        if self.request.POST['industry_type'] == "group":
            researchGroup_form = forms.ResearchGroupBasicInfoForm(self.request.POST, self.request.FILES)
            context['researchGroup_form'] = researchGroup_form
        else:
            RandD_form = forms.RandDBasicInfoForm(self.request.POST, self.request.FILES)
            context['RandD_form'] = RandD_form
        context['form'] = form
        return render(request=self.request, template_name=self.template_name, context=context)
        # return super().form_invalid(form)

    def form_valid(self, form):
        industry_user = models.IndustryUser.objects.get(user=self.request.user)
        if form.cleaned_data["industry_type"] == 'group':
            groupForm = forms.ResearchGroupBasicInfoForm(self.request.POST, self.request.FILES)
            if groupForm.is_valid():
                interfacePerson = form.save()
                groupProfile = groupForm.save(commit=False)
                groupProfile.industry_user = industry_user
                groupProfile.interfacePerson = interfacePerson
                groupProfile.save()
                industry_user.status = 'free'
                industry_user.save()
            else:
                print("Group Form Invalid")
                context = self.get_context_data()
                context['researchGroup_form'] = groupForm
                return render(request=self.request, template_name=self.template_name, context=context)
        else:
            RandDForm = forms.RandDBasicInfoForm(self.request.POST, self.request.FILES)
            if RandDForm.is_valid():
                interfacePerson = form.save()
                RandDProfile = RandDForm.save(commit=False)
                RandDProfile.industry_user = industry_user
                RandDProfile.interfacePerson = interfacePerson
                RandDProfile.save()
                industry_user.status = 'free'
                industry_user.save()
            else:
                print("RandD Form Invalid")
                context = self.get_context_data()
                context['RandD_form'] = RandDForm
                return render(request=self.request, template_name=self.template_name, context=context)
        industryForm = form.save(commit=False)
        industry_user = self.request.user.industryuser
        industryForm.industry_user = industry_user
        industryForm.save()
        industry_user.status = 'free'
        industry_user.save()
        return super().form_valid(form)


class UserInfo(PermissionRequiredMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = 'industry/userInfo.html'
    login_url = '/login/'
    permission_required = ('industry.be_industry',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        industry_user = models.IndustryUser.objects.get(user=self.request.user)
        profile = industry_user.profile
        context['interface_form'] = forms.interfacePersonForm(instance=profile.interfacePerson, )
        if type(profile) == models.RandDProfile:
            context['type_form'] = "R&D"
            context['RandD_form'] = forms.RandDInfoForm(instance=profile,
                                                        initial={'RandD_type': profile.RandD_type})
        else:
            context['type_form'] = "group"
            context['researchgroup_form'] = forms.ResearchGroupInfoForm(instance=profile,
                                                                        initial={'type_group': profile.type_group})
        return context

    def post(self, request):
        industry_user = models.IndustryUser.objects.get(user=self.request.user)
        industryForm = industry_user.profile
        interface_form = forms.interfacePersonForm(request.POST)
        if interface_form.is_valid():
            industryForm.interfacePerson.fullname = interface_form.cleaned_data['fullname']
            industryForm.interfacePerson.position = interface_form.cleaned_data['position']
            industryForm.interfacePerson.phone_number = interface_form.cleaned_data['phone_number']
            industryForm.interfacePerson.email = interface_form.cleaned_data['email']
            industryForm.interfacePerson.save()
            if type(industryForm) == models.RandDProfile:
                form = forms.RandDInfoForm(request.POST, request.FILES)
                if form.is_valid():
                    industryForm.address = form.cleaned_data['address']
                    industryForm.RandD_type = form.cleaned_data['RandD_type']
                    industryForm.tax_declaration = form.cleaned_data['tax_declaration']
                    industryForm.services_products = form.cleaned_data['services_products']
                    industryForm.awards_honors = form.cleaned_data['awards_honors']
                else:
                    print('the R&D errors are:', form.errors)
                    context = self.get_context_data()
                    context['RandD_form'] = form
                    return render(request=request, template_name=self.template_name, context=context)
            else:
                form = forms.ResearchGroupInfoForm(request.POST, request.FILES)
                if form.is_valid():
                    industryForm.address = form.cleaned_data['address']
                    industryForm.type_group = form.cleaned_data['type_group']
                else:
                    # print(form.)
                    print('the ResearchGroup errors are:', form.errors)
                    context = self.get_context_data()
                    context['researchGroup_form'] = form
                    return render(request=request, template_name=self.template_name, context=context)
            if form.cleaned_data['photo']:
                if industryForm.photo:
                    if os.path.isfile(industryForm.photo.path):
                        os.remove(industryForm.photo.path)
                industryForm.photo = form.cleaned_data['photo']
            industryForm.save()
        else:
            print('the interface errors are:', interface_form.errors)
            context = self.get_context_data()
            context['interface_form'] = interface_form
            return render(request=request, template_name=self.template_name, context=context)
        return HttpResponseRedirect(reverse('industry:index'))


class NewProject(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    template_name = 'industry/newProject.html'
    form_class = forms.ProjectForm
    login_url = '/login/'
    permission_required = ('industry.be_industry',)

    def post(self, request, *args, **kwargs):
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            project_title_persian = form.cleaned_data['project_title_persian']
            project_title_english = form.cleaned_data['project_title_english']
            research_methodology = form.cleaned_data['research_methodology']
            main_problem_and_importance = form.cleaned_data['main_problem_and_importance']
            # predict_profit = form.cleaned_data['predict_profit']
            required_lab_equipment = form.cleaned_data['required_lab_equipment']
            approach = form.cleaned_data['approach']
            policy = form.cleaned_data['policy']
            required_budget = form.cleaned_data['required_budget']
            project_phase = form.cleaned_data['project_phase']
            # required_technique = form.cleaned_data['required_technique']
            required_method = form.cleaned_data['required_method']
            progress_profitability = form.cleaned_data['progress_profitability']
            potential_problems = form.cleaned_data['potential_problems']
            new_project_form = models.ProjectForm(project_title_persian=project_title_persian,
                                                  project_title_english=project_title_english,
                                                  research_methodology=research_methodology,
                                                  main_problem_and_importance=main_problem_and_importance,
                                                  #   predict_profit=predict_profit,
                                                  required_lab_equipment=required_lab_equipment,
                                                  required_method=required_method,
                                                  approach=approach,
                                                  policy=policy,
                                                  required_budget=required_budget,
                                                  project_phase=project_phase,
                                                  progress_profitability=progress_profitability,
                                                  potential_problems=potential_problems,
                                                  )
            key_words = form.cleaned_data['key_words'].split(',')
            new_project_form.save()

            for word in key_words:
                new_project_form.key_words.add(models.Keyword.objects.get_or_create(name=word)[0])
            new_project = models.Project(project_form=new_project_form, industry_creator=request.user.industryuser)
            new_project.save()
            subject = 'ثبت پروژه جدید'
            message = """با سلام و احترام
            کاربر صنعت با نام کاربری {}
            پروژه جدید به نام {} را در تاریخ {} ثبت نموده است.
            با تشکر""".format(request.user.username, project_title_persian, JalaliDate(datetime.date.today()))
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER, "sepehr.metanat@gmail.com", ],
                    fail_silently=False
                )
            except TimeoutError:
                return HttpResponse('Timeout Error!!')
            return HttpResponseRedirect(reverse('industry:index'))
        return super().post(request, *args, **kwargs)


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    template_name = 'industry/project_list.html'
    login_url = '/login/'
    permission_required = ('industry.be_industry',)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        industry = get_object_or_404(models.IndustryUser, user=self.request.user)
        context['industry'] = industry
        if industry.profile:
            context['photo'] = industry.profile.photo
        return context


def checkUserId(request, userId):
    if models.IndustryUser.objects.filter(userId=userId).count():
        return False
    return True


def ProjectSetting(request):
    technique_list = request.POST.getlist('technique')
    if len(technique_list) == 0:
        return JsonResponse({
            'message': 'متاسفانه بدون انتخاب تکنیک‌های موردنظر، امکان ارسال درخواست وجود ندارد.',
        }, status=400)
    project = models.Project.objects.filter(pk=request.POST['projectId'])
    for technique in technique_list:
        project_technique = Technique.objects.get_or_create(technique_title=technique[:-2])
        project.projectform.techniques.add(project_technique[0])
    project.projectform.save()
    expertId = request.POST['expertId']
    expert = ExpertUser.objects.filter(userId=expertId)
    data = {}
    if expert.autoAddProject:
        project.expert_accepted = expert
        data['addExpert'] = True
        message="""با سلام
مجموعه پژوهشی «{industryName}» تقاضای پیوستن شما به پروژه «{projectName}» را داشته‌اند.
با توجه به این که قابلیت پیوستن شما به پروژه‌ها (تنها با / بدون) اجازه شما فراهم است، (از طریق قسمت «پیام‌ها» می‌توانید درخواست‌شان را قبول و یا رد کنید / شما به این پروژه اضافه شدید). 
لطفا برای بررسی پروژه مذکور، حساب کاربری‌تان را بررسی بفرمایید.
در ضمن، شما می‌توانید برای تغییر این قابلیت، قسمت «اطلاعات کاربری» حساب کاربری‌تان را نیز مشاهده بفرمایید.
با آرزوی موفقیت، 
چمران‌تیم""".format({"industryName" : project.industry_creator.profile.name,
                    "projectName"  : project.project_title_persian})
        subject = 'تقاضای پیوستن به پروژه'
        html_templateForAdmin = get_template('registration/projectRequest_template.html')
        email_templateForAdmin = html_templateForAdmin.render({'message': message})
        email = EmailMultiAlternatives(subject=subject, from_email=settings.EMAIL_HOST_USER,
                                    to=[expert.user.get_username(), "sepehr.metanat@gmail.com"])
        email.attach_alternative(email_templateForAdmin, 'text/html')
        email.send()
        # try:
        #     send_mail(
        #         subject=subject,
        #         message=message,
        #         from_email=settings.EMAIL_HOST_USER,
        #         recipient_list=[expert.user.get_username(), "sepehr.metanat@gmail.com", ],
        #         fail_silently=False
        #     )
        # except TimeoutError:
        #     return HttpResponse('Timeout Error!!')
        newMessage = Message(title=subject,
                            text=message,
                            type=0)
        newMessage.save()
        newMessage.receiver.add(expert)
    else: 
        data['addExpert'] = False
    project.save()
    return JsonResponse(data={})


def searchUserId(request):
    searchKey = request.POST['searchKey']
    suggestedExperts = ExpertUser.objects.filter(userId__contain=searchKey).values('userId')
    data = {"expertId": suggestedExperts}
    return JsonResponse(data=data)

def preview_project(request):
    return render(request, 'industry/preview_project.html', {})
