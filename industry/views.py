import datetime
import os
import re

from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.exceptions import PermissionDenied
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
from expert.models import ExpertUser, RequestResearcher
from expert.views import showAllTechniques
from expert.forms import RequestResearcherForm
from researcher.models import Technique, RequestedProject, ResearcherUser
from chamran_admin.models import Message

USER_ID_PATTERN = re.compile('[\w]+')

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
    
    tempTech = []
    for tech in data['techniques']:
        tempTech.append(tech.technique_title)
    data["techniques"] = tempTech
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
    data['project'] = project
    data['project_pk'] = project.id
    # data['expert_pk'] = project.expert_accepted.id
    industryform = request.user.industryuser.profile
    data['projectForm'] = model_to_dict(project.project_form)
    projectDate = {
     "start":   gregorian_to_numeric_jalali(project.date_start),
     "firstPhase":   gregorian_to_numeric_jalali(project.date_project_started),
     "secondPhase":   gregorian_to_numeric_jalali(project.date_phase_two_deadline),
     "thirdPhase":  gregorian_to_numeric_jalali(project.date_phase_three_deadline),
     "finished":   gregorian_to_numeric_jalali(project.date_finished),
    }
    data['timeScheduling'] = projectDate
    data['title'] = project.project_form.persian_title
    data['eng_title'] = project.project_form.english_title
    data["industry_name"] = industryform.name
    if industryform.photo:
        data["industry_logo"] = industryform.photo.url
    data['enforcers'] = []
    for expert in project.expert_accepted.all():
        expertData = {
            "name": str(expert.expertform),
            "id": expert.pk
        }
        if expert.expertform.photo:
            expertData['photo'] = expert.expertform.photo.url
        data['enforcers'].append(expertData)
    # data['enforcer_name'] = str(project.expert_accepted.expertform)
    # data['enforcer_id'] = project.expert_accepted.pk
    data["executive_info"] = project.executive_info
    data["budget_amount"] = project.project_form.required_budget

    data['comments'] = []
    for comment in Comment.objects.filter(project=project).exclude(industry_user=None):
        try:
            url = comment.attachment.url
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
    evaluation_history = project.industry_creator.expertevaluateindustry_set.filter(project=project)
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

    data["techniques"] = []
    # }
    # projectRequest = expert_models.ExpertRequestedProject.objects.filter(project=project).filter(
    #     expert=project.expert_accepted).first()
    for technique in project.project_form.techniques.all():
        data["techniques"].append(technique.__str__())

    return data


# is called by an ajax request and returns the necessary information to display the project on the front-end
@permission_required('industry.be_industry', login_url='/login/')
def show_project_ajax(request):
    project = models.Project.objects.filter(id=request.GET.get('id')).first()
    if project.status == 1 or project.status == 0:
        data = usualShow(request, project)
        return JsonResponse(data)
    else:
        return JsonResponse(data={"error": "This porjct is accepted by an expert."}, status=400)


@permission_required('industry.be_industry', login_url='/login/')
def GetComment(request):
    project_id = request.GET.get('project_id')
    project = get_object_or_404(models.Project, pk=project_id)
    all_comments = models.Comment.objects.filter(project=project)
    if "expert_id"  in request.GET.keys():
        expert = get_object_or_404(ExpertUser, pk=request.GET.get('expert_id'))
        comments = all_comments.filter(expert_user=expert).exclude(industry_user=None)
    elif "researcher_id"  in request.GET.keys():
        researcher = get_object_or_404(ResearcherUser, pk=request.GET.get('researcher_id'))
        comments = all_comments.filter(researcher_user=researcher).exclude(industry_user=None)
    else:
        return JsonResponse(data={"message": "Didn't send researcher or expert id"}, status=400)
    response = []
    for comment in comments:
        try:
            url = comment.attachment.url
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
        if comment.sender_type != 'industry':
            comment.status = "seen"
            comment.save()
    # if project.expert_accepted:
    if expert in project.expert_accepted.all():
        data = {
            'comment': response,
            'accepted': True,
            'enforcer': True
        }
    elif expert in project.expert_applied.all():
        data = {
            'comment': response,
            'accepted': False,
            'applied': True
        }
    elif project.expert_accepted.all().count:
        data = {
            'comment': response,
            'accepted': True,
            'enforcer': False,
            'applied': False
        }
    else:
        data = {
            'comment': response,
            'accepted': False,
            'accepted': False,
            'applied': False
        } 
    return JsonResponse(data=data)


@permission_required('industry.be_industry', login_url='/login/')
def accept_project(request):
    expert = ExpertUser.objects.filter(pk=request.POST['expert_id']).first()
    project = models.Project.objects.filter(pk=request.POST['project_id']).first()
    project.expert_accepted.add(expert)
    project.date_start = datetime.date.today()
    project.status = 2
    project.save()
    expert.status = 'involved'
    expert.save()
    requestPorject = expert_models.ExpertRequestedProject.objects.get(expert=expert)
    project_form = project.project_form
    for tech in requestProject.required_technique.all():
        if tech not in project_form.techniques.all():
            project_form.techniques.add(tech)
    project_form.save()
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
        description = form.cleaned_data['description']
        attachment = form.cleaned_data['attachment']
        if "expert_id" in request.POST.keys():
            expert_user = get_object_or_404(ExpertUser, pk=request.POST['expert_id'])
            new_comment = Comment.objects.create(project=project,
                                                industry_user=request.user.industryuser,
                                                sender_type="industry",
                                                expert_user=expert_user,
                                                description=description,
                                                attachment=attachment,
                                                status='unseen')
        elif "researcher_id" in request.POST.keys():
            researcher_user = get_object_or_404(ResearcherUser, pk=request.POST['researcher_id'])
            new_comment = Comment.objects.create(project=project,
                                                industry_user=request.user.industryuser,
                                                sender_type="industry",
                                                researcher_user=researcher_user,
                                                description=description,
                                                attachment=attachment,
                                                status='unseen')
        else:
            return JsonResponse(data={'message': "Didn\'t send any id."}, status=400)
        new_comment.save()
        if attachment is not None:
            url = new_comment.attachment.url
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
        industry_user = self.request.user.industryuser
        if industry_user.status != 'signed_up':
            context['projects'] = models.Project.objects.filter(industry_creator=industry_user)
        else:
            context['RandD_form'] = forms.RandDBasicInfoForm
            context['researchGroup_form'] = forms.ResearchGroupBasicInfoForm
        return context

    def form_invalid(self, form):
        context = self.get_context_data()
        context['form_filled'] = None
        if self.request.POST['industry_type'] == "group":
            researchGroup_form = forms.ResearchGroupBasicInfoForm(self.request.POST, self.request.FILES)
            context['researchGroup_form'] = researchGroup_form
            context['form_filled'] = "researchGroup"
        else:
            RandD_form = forms.RandDBasicInfoForm(self.request.POST, self.request.FILES)
            context['RandD_form'] = RandD_form
            context['form_filled'] = "RandD_form"
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
                RandDProfile.name = RandDForm.cleaned_data['RandDname']
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
                                                        initial={
                                                            'RandD_type': profile.RandD_type,
                                                            "RandDname": profile.name})
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
                    industry_user.userId = form.cleaned_data['userId']                    
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
                    industry_user.userId = form.cleaned_data['userId']
                else:
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
            industry_user.save()
        else:
            print('the interface errors are:', interface_form.errors)
            context = self.get_context_data()
            context['interface_form'] = interface_form
            return render(request=request, template_name=self.template_name, context=context)
        return HttpResponseRedirect(reverse('industry:userInfo'))


class NewProject(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    template_name = 'industry/newProject.html'
    form_class = forms.ProjectForm
    login_url = '/login/'
    permission_required = ('industry.be_industry',)

    def post(self, request, *args, **kwargs):
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            persian_title = form.cleaned_data['persian_title']
            english_title = form.cleaned_data['english_title']
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
            new_project_form = models.ProjectForm(persian_title=persian_title,
                                                  english_title=english_title,
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
            با تشکر""".format(request.user.username, persian_title, JalaliDate(datetime.date.today()))
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

@permission_required('industry.be_industry', login_url='/login/')
def checkUserId(request):
    if request.is_ajax() and request.method == "POST":
        user_id = request.POST.get("user_id")
        if not bool(USER_ID_PATTERN.match(user_id)):
            return JsonResponse({"invalid_input": True})
        if user_id != request.user.industryuser:
            if models.IndustryUser.objects.filter(userId=user_id).count():
                return JsonResponse({"is_unique": False, "invalid_input": False})
        return JsonResponse({"is_unique": True, "invalid_input": False})

@permission_required('industry.be_industry', login_url='/login/')
def ProjectSetting(request):
    if request.method == "GET":
        project = models.Project.objects.get(id=request.GET.get('id'))
        data = {
            "techniques": showAllTechniques(),
            "projectTechniques": [],
            "requestResearcher": project.reseacherRequestAbility,
             }
        for tech in project.project_form.techniques.all():
            data['projectTechniques'].append(tech.technique_title)
        data['acceptedExpert'] = []
        for expert in project.expert_accepted.all():
            expertData = { 
                "id": expert.pk,
                "fullname": expert.expertform.__str__(),
                "userId"  : expert.userId,
                "accepted": True,
            }
            if expert.expertform.photo:
                expertData['photo'] = expert.expertform.photo.url
            data['acceptedExpert'].append(expertData)
        data['suggestedExpert'] = []
        for expert in project.expert_suggested.all():
            expertData = { 
                "id": expert.pk,
                "fullname": expert.expertform.__str__(),
                "userId"  : expert.userId,
                "accepted": False,
            }
            if expert.expertform.photo:
                expertData['photo'] = expert.expertform.photo.url
            data['suggestedExpert'].append(expertData)
        return JsonResponse(data=data)
    elif request.method == "POST":
        print(request.POST)
        expert_ids = request.POST.getlist('expert_ids')
        # expertId = request.POST['uuid']
        if len(expert_ids) == 0:
            return JsonResponse({
                'expertId': 'استاد نمی تواند خالی باشد.',
            }, status=400)
        technique_list = request.POST.getlist('technique')
        if len(technique_list) == 0:
            return JsonResponse({
                'message': 'متاسفانه بدون انتخاب تکنیک‌های موردنظر، امکان ارسال درخواست وجود ندارد.',
            }, status=400)
        project = models.Project.objects.get(id=request.POST['id'])
        projectform = project.project_form
        if 'requestResearcher' in request.POST.keys():
            project.reseacherRequestAbility = request.POST['requestResearcher']
        else:
            project.reseacherRequestAbility = False
        projectform.techniques.clear()
        for technique in technique_list:
            projectform.techniques.add(Technique.objects.get_or_create(\
                                               technique_title=technique[:-2])[0])
        projectform.save()
        data = {"experts": []}
        for expert_id in expert_ids:
            expert = ExpertUser.objects.get(id=expert_id)
            expertResult = {"id": expert}
            if expert in project.expert_accepted.all():
                expertResult['addExpert'] = True
                continue
            elif expert in project.expert_suggested.all():
                expertResult['addExpert'] = False
                continue
            if expert.autoAddProject:
                project.expert_accepted.add(expert)
                project.date_start = datetime.date.today()
                project.status = 2
                expert.status = 'involved'
                expert.save()
                expertResult['addExpert'] = True
                message="""با سلام
    مجموعه پژوهشی «{industryName}» تقاضای پیوستن شما به پروژه «{projectName}» را داشته‌اند.
    با توجه به این که قابلیت پیوستن شما به پروژه‌ها بدون اجازه شما فراهم است، شما به این پروژه اضافه شدید. 
    لطفا برای بررسی پروژه مذکور، حساب کاربری‌تان را بررسی بفرمایید.
    در ضمن، شما می‌توانید برای تغییر این قابلیت، قسمت «اطلاعات کاربری» حساب کاربری‌تان را نیز مشاهده بفرمایید.
    با آرزوی موفقیت، 
    چمران‌تیم""".format(industryName=project.industry_creator.profile.name,
                    projectName=project.project_form.persian_title)
            else: 
                expertResult['addExpert'] = False
                project.expert_suggested.add(expert)
                message="""با سلام
        مجموعه پژوهشی «{industryName}» تقاضای پیوستن شما به پروژه «{projectName}» را داشته‌اند.
        با توجه به این که قابلیت پیوستن شما به پروژه‌ها تنها با اجازه شما فراهم است، از طریق قسمت «پیام‌ها» می‌توانید درخواست‌شان را قبول و یا رد کنید . 
        لطفا برای بررسی پروژه مذکور، حساب کاربری‌تان را بررسی بفرمایید.
        در ضمن، شما می‌توانید برای تغییر این قابلیت، قسمت «اطلاعات کاربری» حساب کاربری‌تان را نیز مشاهده بفرمایید.
        با آرزوی موفقیت، 
        چمران‌تیم""".format(industryName=project.industry_creator.profile.name,
                        projectName=project.project_form.persian_title)
            models.ProjectForm.persian_title
            subject = 'تقاضای پیوستن به پروژه'
            html_templateForAdmin = get_template('registration/projectRequest_template.html')
            email_templateForAdmin = html_templateForAdmin.render({'message': message})
            email = EmailMultiAlternatives(subject=subject, from_email=settings.EMAIL_HOST_USER,
                                        to=[expert.user.get_username(), ])
            email.attach_alternative(email_templateForAdmin, 'text/html')
            email.send()
            newMessage = Message(title=subject,
                                    text=message,
                                    type=0)
            newMessage.save()
            newMessage.receiver.add(expert.user)
            data['experts'].append(expertResult)
        project.save()
        return JsonResponse(data={"message": "تنظیمات با موفقیت ثبت شد."})

def searchUserId(request):
    searchKey = request.POST['searchKey']
    suggestedExperts = ExpertUser.objects.filter((Q(userId__icontains=searchKey)| \
                                                Q(expertform__fullname__icontains=searchKey)))
    data = {"experts": []}
    for expert in suggestedExperts:
        expertData = {
            "userId" : expert.userId,
            "id" : expert.pk,
            "fullname" : expert.expertform.fullname,
            "autoAdd" : expert.autoAddProject,
        }
        if expert.expertform.photo:
            expertData['photo'] = expert.expertform.photo.url
        data['experts'].append(expertData)
    return JsonResponse(data=data)

class show_active_project(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = "industry/preview_project.html"
    permission_required = ('industry.be_industry',)
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(models.Project, code=kwargs["code"])
        if project.industry_creator.user != request.user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(models.Project, code=kwargs["code"])
        context = ActiveProject(request=self.request, project=project, data=context)
        context['researcher_accepted'] = []
        for researcher in project.researcher_accepted.all():
            researcher = {
                "id": researcher.pk,
                "fullname": researcher.researcherprofile.fullname,
                "photo": researcher.researcherprofile.photo                
            }
            context['researcher_accepted'].append(researcher)
        context['researchers_applied'] = []
        researcherRequested = RequestedProject.objects.filter(project=project)
        for requested in researcherRequested:
            researcher = requested.researcher
            researcher_applied = {
                'id': researcher.pk,
                "fullname": researcher.researcherprofile.fullname,
                "photo": researcher.researcherprofile.photo,
                "status": requested.status 
            }
            if requested.status == "unseen":
                requested.status = "pending"
                requested.save()
            context['researchers_applied'].append(researcher_applied)
        context['reseacherRequestAbility'] = project.reseacherRequestAbility
        if project.reseacherRequestAbility:
            try:
                requestResearcher = RequestResearcher.objects.get(project=project)
                context['researcherRequestFrom'] = RequestResearcherForm(initial={
                                                    "least_hour" : requestResearcher.least_hour,
                                                    "researcher_count": requestResearcher.researcher_count})
            except:
                context['researcherRequestFrom'] = RequestResearcherForm()
        return context

@permission_required('expert.be_industry', login_url='/login/')
def industryRequestResearcher(request):
    project = models.Project.objects.get(id=request.POST['project_id'])
    form = RequestResearcherForm(request.POST)
    if form.is_valid():
        expert = project.expert_accepted.all().first()
        least_hour = form.cleaned_data['least_hour']
        researcher_count = form.cleaned_data['researcher_count']
        try:
            researcher_request = RequestResearcher.objects.get(project=project)
            researcher_request.researcher_count = researcher_count
            researcher_request.least_hour = least_hour
            researcher_request.save()
        except:
            researcher_request = RequestResearcher(project=project
                                                   , expert=expert
                                                   , researcher_count=researcher_count
                                                   , least_hour=least_hour)

            researcher_request.save()

        return JsonResponse({"successfull": "successfull"})
    else:
        return JsonResponse(data=form.errors, status=400)    

# def show_active_project(request, code):
#     project = get_object_or_404(models.Project, code=kwargs["code"])
#     ActiveProject(request)
