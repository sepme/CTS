import datetime
import os

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.forms import model_to_dict
from django.views import generic, View
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

from persiantools.jdatetime import JalaliDate

from ChamranTeamSite import settings
from industry.models import IndustryForm, Comment
from expert import models as expert_models
from . import models ,forms
from expert.models import ExpertUser

# function name says it all :)
def gregorian_to_numeric_jalali(date):
    if date :
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
    data['required_technique']=[]
    evaluation_history = request.user.industryuser.expertevaluateindustry_set.filter(project=project)
    data['status']     = project.status
    data['accepted']   = False
    data['vote']       = False

    data['expert_messaged'] = []
    for expert in project.expert_messaged.all():
        data['expert_messaged'].append({
            'id': expert.id,
            'name': expert.expertform.__str__(),
            'applied' : expert in project.expert_applied.all(),
        })
    for expert in project.expert_applied.all():
        if expert not in project.expert_messaged.all():
            data['expert_messaged'].append({
                'id': expert.id,
                'name': expert.expertform.__str__(),
                'applied' : expert in project.expert_applied.all(),
            })
    return data

def ActiveProject(request, project, data):
    data['accepted'] = True
    data['comments'] = []
    for comment in Comment.objects.filter(project=project).exclude(industry_user=None):
        try:
            url = comment.attachment.url.split("/")[-1]
        except:
            url = "None"
        data['comments'].append({
            'id': comment.id,
            'text': comment.description,
            'sender_type': comment.sender_type,
            'attachment': url,
            'pk' : comment.pk,
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
    
    industryform = request.user.industryuser.industryform
    projectDate = [
        gregorian_to_numeric_jalali(project.date_start),
        gregorian_to_numeric_jalali(project.date_project_started),
        gregorian_to_numeric_jalali(project.date_phase_two_deadline),
        gregorian_to_numeric_jalali(project.date_phase_three_deadline),
        gregorian_to_numeric_jalali(project.date_finished),
    ]
    data['timeScheduling'] = projectDate
    # data = {
    data["industry_name"]  = industryform.name
    data["industry_logo"]  = industryform.photo.url
    data['enforcer_name']  = str(project.expert_accepted.expertform)
    data['enforcer_id']    = project.expert_accepted.pk
    data["executive_info"] = project.executive_info
    data["budget_amount"]  = project.project_form.required_budget
    data["techniques"]     = []
    # }
    projectRequest = expert_models.ExpertRequestedProject.objects.filter(project=project).filter(expert=project.expert_accepted).first()
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
    expert_id  = request.GET.get('expert_id')
    project_id = request.GET.get('project_id')
    project = get_object_or_404(models.Project ,pk=project_id)
    expert  = get_object_or_404(ExpertUser ,pk=expert_id)
    all_comments = models.Comment.objects.filter(project=project)
    comments = all_comments.filter(expert_user=expert).exclude(industry_user=None)    
    response = []
    for comment in comments:
        try:
            url = comment.attachment.url.split("/")[-1]
        except:
            url = "None"
        temp = {
            'pk'           : comment.pk,
            'text'  : comment.description,
            'replied_text' : comment.replied_text,
            'sender_type'  : comment.sender_type,
            'attachment'   : url
        }
        response.append(temp)    
        if comment.sender_type == 'expert' or comment.sender_type == 'system':
            comment.status = "seen"
            comment.save()
    if project.expert_accepted :
        if project.expert_accepted == expert:
            data = {
            'comment'  : response,
            'accepted' : True,
            'enforcer' : True
            }
        else:
            data = {
                'comment'  : response,
                'accepted' : True,
                'enforcer' : False
                }
        return JsonResponse(data=data)
    if expert in project.expert_applied.all():
        data = {
            'comment' : response,
            'accepted' : False,
            'applied' : True
            }
    else:
        data = {
            'comment' : response,
            'accepted' : False,
            'applied' : False
            }
    return JsonResponse(data=data)

@permission_required('industry.be_industry', login_url='/login/')
def accept_project(request):
    expert  = ExpertUser.objects.filter(pk=request.POST['expert_id']).first()
    project = models.Project.objects.filter(pk=request.POST['project_id']).first()
    project.expert_accepted = expert
    project.date_start = datetime.date.today()
    project.status = 2
    project.save()
    expert.status = 'involved'
    expert.save()
    data = {'success' : 'successful'}
    return JsonResponse(data=data)

@permission_required('industry.be_industry', login_url='/login/')
def refuse_expert(request):
    expert  = ExpertUser.objects.filter(pk=request.POST['expert_id']).first()
    project = models.Project.objects.filter(pk=request.POST['project_id']).first()
    project.expert_banned.add(expert)
    project.save()
    data = {'success' : 'successful'}
    return JsonResponse(data=data)

# this function is called when the industry user comments on a project
@permission_required('industry.be_industry', login_url='/login/')
def submit_comment(request):
    form = forms.CommentForm(request.POST ,request.FILES)
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
            data = {
                'success' : 'successful',
                'attachment' : new_comment.attachment.url.split("/")[-1],
                'description':description,
            }
        else:
            data = {
                'success' : 'successful',
                'attachment' : "None",
                'description': description,
            }
        return JsonResponse(data=data)
    return JsonResponse(data=form.errors ,status=400)

# main page for an industry user
class Index(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'industry/index.html'
    login_url = '/login/'
    permission_required = ('industry.be_industry',)

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and \
                models.IndustryUser.objects.filter(user=self.request.user).count() and \
                self.request.user.industryuser.status == 'signed_up':
            context['form'] = forms.IndustryBasicInfoForm(self.request.user)
        else:
            industry_user = self.request.user.industryuser
            context['projects'] = models.Project.objects.filter(industry_creator=industry_user)
        return context

    # submitting the initial info form
    def post(self, request, *args, **kwargs):
        form = forms.IndustryBasicInfoForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data['photo']
            name = form.cleaned_data['name']
            registration_number = form.cleaned_data['registration_number']
            date_of_foundation = form.cleaned_data['date_of_foundation']
            research_field = form.cleaned_data['research_field']
            industry_type = form.cleaned_data['industry_type']
            industry_address = form.cleaned_data['industry_address']
            phone_number = form.cleaned_data['phone_number']
            email_address = form.cleaned_data['email_address']
            industry_user = request.user.industryuser
            industry_info = models.IndustryForm(industry_user=industry_user,
                                                name=name,
                                                registration_number=registration_number,
                                                date_of_foundation=date_of_foundation,
                                                research_field=research_field,
                                                industry_type=industry_type,
                                                industry_address=industry_address,
                                                phone_number=phone_number,
                                                email_address=email_address)            
            industry_info.photo.save(photo.name, photo)
            industry_info.save()
            if not industry_info.photo:
                with open(os.path.join(settings.BASE_DIR, 'industry/static/industry/img/profile.jpg'),
                          'rb') as image_file:
                    default_image = image_file.read()
                    industry_info.photo.save('profile.jpg', ContentFile(default_image))
            industry_user.status = 'free'
            industry_user.save()
            return HttpResponseRedirect(reverse('industry:index'))
        return render(request, 'industry/index.html', context={'form': form})


class UserInfo(PermissionRequiredMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = 'industry/userInfo.html'
    login_url = '/login/'
    permission_required = ('industry.be_industry',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.IndustryInfoForm(self.request.user,
                                           instance=self.request.user.industryuser.industryform,
                                           initial={
                                               'industry_type':
                                                   self.request.user.industryuser.industryform.industry_type})
        return context

    def post(self, request):
        form = forms.IndustryInfoForm(self.request.user, request.POST, request.FILES,
                                      initial={
                                          'industry_type': self.request.user.industryuser.industryform.industry_type})
        if form.is_valid():
            # model_form = form.save(commit=False)
            industryForm = IndustryForm.objects.get(name=form.cleaned_data['name'])
            industryForm.industry_type=form.cleaned_data['industry_type']
            industryForm.tax_declaration=form.cleaned_data['tax_declaration']
            industryForm.services_products=form.cleaned_data['services_products']
            industryForm.awards_honors=form.cleaned_data['awards_honors']
            # )
            if form.cleaned_data['photo']:
                if os.path.isfile(industryForm.photo.path):
                    os.remove(industryForm.photo.path)
                # industryForm.photo.save(form.cleaned_data['photo'].name, form.cleaned_data['photo'])
                industryForm.photo = form.cleaned_data['photo']
            industryForm.save()
            return HttpResponseRedirect(reverse('industry:index'))
        else:
            print('the errors are:', form.errors)
        return render(request, 'industry/userInfo.html', context={'form': form})


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
            predict_profit = form.cleaned_data['predict_profit']
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
                                                  predict_profit=predict_profit,
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
            message ="""با سلام و احترام
            کاربر صنعت با نام کاربری {}
            پروژه جدید به نام {} را در تاریخ {} ثبت نموده است.
            با تشکر""".format(request.user.username ,project_title_persian,JalaliDate(datetime.date.today()))
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER,"sepehr.metanat@gmail.com",],
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
        if industry.industryform:
            context['photo'] = industry.industryform.photo
        return context
