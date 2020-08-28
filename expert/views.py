from django.views import generic
# from django.views import View
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, get_object_or_404, Http404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.core import serializers
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template
from django.forms import model_to_dict
from django.core.exceptions import PermissionDenied

from persiantools.jdatetime import JalaliDate
from datetime import datetime
from itertools import chain
import json, re

from . import forms, webScraping
from .models import *

from industry.models import *
from researcher.models import ScientificRecord as ResearcherScientificRecord
from researcher.models import ExecutiveRecord as ResearcherExecutiveRecord
from researcher.models import ResearcherUser, ResearcherProfile, Technique, \
                              StudiousRecord, TechniqueInstance, RequestedProject
from chamran_admin.models import Message

USER_ID_PATTERN = re.compile("[\w]+$")

def gregorian_to_numeric_jalali(date):
    if date is None:
        return "نامشخص"
    j_date = JalaliDate(date)
    return str(j_date.year) + '/' + str(j_date.month) + '/' + str(j_date.day)


def calculate_deadline(finished, started):
    if finished is None or started is None:
        return 'تاریخ نامشخص'
    diff = JalaliDate(finished) - JalaliDate(started)
    days = diff.days
    if days < 0:
        return None
    elif days < 7:
        return '{} روز'.format(days)
    elif days < 30:
        return '{} هفته'.format(int(days / 7))
    elif days < 365:
        return '{} ماه'.format(int(days / 30))
    else:
        return '{} سال'.format(int(days / 365))


class Index(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    template_name = 'expert/index.html'
    login_url = "/login/"
    permission_required = ("expert.be_expert",)
    form_class = forms.InitialInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expert_user = get_object_or_404(ExpertUser, user=self.request.user)

        if expert_user.status != "signed_up":
            allProjects = Project.objects.filter(status=1).exclude(expert_banned=expert_user)
            context['allProjects'] = allProjects
            newProjects = allProjects.exclude(expert_applied__in=[expert_user,]).exclude(expert_accepted=expert_user)
            context['newProjects'] = newProjects
            appliedProjects = allProjects.filter(expert_applied__in=[expert_user,]).exclude(expert_accepted=expert_user)
            context['appliedProjects'] = appliedProjects
            context['activeProjects'] = Project.objects.filter(status=2).filter(expert_accepted=expert_user)
            context['doneProjects'] = ExpertProjectHistory.objects.filter(expert=expert_user)
        return context

    def form_valid(self, form):
        expert_user = get_object_or_404(ExpertUser, user=self.request.user)
        try:
            expert_form = expert_user.expertform
            if expert_form :
                expert_form.photo = form.cleaned_data['photo']
                expert_form.fullname = form.cleaned_data['fullname']
                expert_form.national_code = form.cleaned_data['national_code']
                expert_form.special_field = form.cleaned_data['special_field']
                expert_form.scientific_rank = form.cleaned_data['scientific_rank']
                expert_form.university = form.cleaned_data['university']
                expert_form.home_number = form.cleaned_data['home_number']
                expert_form.phone_number = form.cleaned_data['phone_number']
        except:
            expert_form = form.save(commit=False)
        expert_form.expert_user = expert_user
        expert_form.email = expert_user.user.get_username()
        expert_form.save()
        expert_user.userId = form.cleaned_data['userId']
        expert_user.status = 'free'
        expert_user.save()
        return HttpResponseRedirect(reverse('expert:index'))


class ResearcherRequest(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'expert/researcherRequest.html'
    login_url = '/login/'
    permission_required = ("expert.be_expert",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expert_user = get_object_or_404(ExpertUser, user=self.request.user)
        projects_list = Project.objects.filter(expert_accepted=expert_user)
        projects_data = []
        for project in projects_list:
            researchers_applied = []
            researcherRequested = RequestedProject.objects.filter(project=project)
            researchers = []
            for requested in researcherRequested:
                researcher = requested.researcher
                researchers.append(researcher)
                techniques = [tech.technique.technique_title for tech in
                                researcher.techniqueinstance_set.all()]
                researcher_applied = {
                    'id'        : researcher.pk,
                    'profile'   : researcher.researcherprofile,
                    'techniques': techniques,   
                    "status"    : requested.status 
                }
                if requested.status == "unseen":
                    requested.status = "pending"
                    requested.save()
                researchers_applied.append(researcher_applied)
            
            for com in Comment.objects.filter(project=project).exclude(researcher_user=None):
                if com.researcher_user not in researchers:
                    researchers.append(com.researcher_user)
            if len(researchers) == 0:
                continue
            # for researcher in researchers:
            #     techniques = [tech.technique.technique_title for tech in
            #                     researcher.techniqueinstance_set.all()]
            #     researcher_applied = {
            #         'id'        : researcher.pk,
            #         'profile'   : researcher.researcherprofile,
            #         'techniques': techniques,
            #     }
            #     researchers_applied.append(researcher_applied)
            appending = {
                'project': project.project_form.persian_title,
                'id': project.pk,
                "researchers_applied": researchers_applied
            }
            projects_data.append(appending)
        context = {}
        if len(projects_data) != 0:
            context = {'applications': projects_data}
        return context


class Questions(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'expert/questions.html'
    login_url = '/login/'
    permission_required = ("expert.be_expert",)

    def get(self, request, *args, **kwargs):
        expert_user = request.user.expertuser
        research_questions = ResearchQuestion.objects.filter(expert=expert_user)
        context = {
            'research_question_form': forms.ResearchQuestionForm(),
            'research_questions': research_questions,
        }
        return render(request, self.template_name, context)


class UserInfo(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    template_name = "expert/userInfo.html"
    form_class = forms.ExpertInfoForm
    model = ExpertForm
    login_url = '/login/'
    success_url = "/expert/userInfo"
    permission_required = ('expert.be_expert',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expert = self.request.user.expertuser
        expertForm = get_object_or_404(ExpertForm, expert_user=expert)
        context['expert_info_form'] = self.form_class(instance=expertForm, initial={"userId":expert.userId})
        context['scientific_instance'] = ScientificRecord.objects.filter(expert_form=expertForm)
        context['executive_instance'] = ExecutiveRecord.objects.filter(expert_form=expertForm)
        context['research_instance'] = ResearchRecord.objects.filter(expert_form=expertForm)
        context['paper_instance'] = PaperRecord.objects.filter(expert_form=expertForm)
        context['keywords'] = expertForm.get_keywords()
        context['expert_form'] = expertForm
        context['scientific_form'] = forms.ScientificRecordForm()
        context['executive_form'] = forms.ExecutiveRecordForm()
        context['research_form'] = forms.ResearchRecordForm()
        context['paper_form'] = forms.PaperRecordForm()
        context['email'] = self.request.user.get_username()
        context['autoAddProject'] = expertForm.expert_user.autoAddProject
        if expertForm.resume:
            context['resume'] = expertForm.resume
        return context

    def form_valid(self, form):
        expertForm = get_object_or_404(ExpertForm, expert_user=self.request.user.expertuser)
        expert_user = expertForm.expert_user
        if self.request.POST.get('autoAddProject'):
            expert_user.autoAddProject = True
        else:
            expert_user.autoAddProject = False
        expert_user.userId = form.cleaned_data['userId']
        expert_user.save()
        expertForm.university = form.cleaned_data['university']
        expertForm.home_address = form.cleaned_data['home_address']
        expertForm.home_number = form.cleaned_data['home_number']
        expertForm.phone_number = form.cleaned_data['phone_number']
        if form.cleaned_data['awards']:
            expertForm.awards = form.cleaned_data['awards']

        if form.cleaned_data['number_of_grants']:
            expertForm.number_of_grants = form.cleaned_data['number_of_grants']

        if form.cleaned_data['languages']:
            expertForm.languages = form.cleaned_data['languages']

        if form.cleaned_data['method_of_introduction']:
            expertForm.method_of_introduction = form.cleaned_data['method_of_introduction']

        if form.cleaned_data['has_industrial_research']:
            expertForm.has_industrial_research = form.cleaned_data['has_industrial_research']

        if form.cleaned_data['number_of_researcher']:
            expertForm.number_of_researcher = form.cleaned_data['number_of_researcher']

        if form.cleaned_data['resume']:
            expertForm.resume = form.cleaned_data['resume']

        photo = self.request.FILES.get('photo')
        if photo is not None:
            if expertForm.photo:
                if os.path.isfile(expertForm.photo.path):
                    os.remove(expertForm.photo.path)
            expertForm.photo = photo

        expertForm.save()
        for word in self.request.POST['keywords'].split(','):
            expertForm.keywords.add(Keyword.objects.get_or_create(name=word)[0])
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     expertForm = get_object_or_404(ExpertForm, expert_user=self.request.user.expertuser)
    #     self.form = forms.ExpertInfoForm(request.POST, request.FILES)
    #     if self.form.is_valid():
    #         expertForm.university   = self.form.cleaned_data['university']
    #         expertForm.home_address = self.form.cleaned_data['home_address']
    #         expertForm.phone_number = self.form.cleaned_data['phone_number']
    #         expertForm.mobile_phone = self.form.cleaned_data['mobile_phone']
    #         if self.form.cleaned_data['awards']:
    #             expertForm.awards = self.form.cleaned_data['awards']

    #         if self.form.cleaned_data['number_of_grants']:
    #             expertForm.number_of_grants = self.form.cleaned_data['number_of_grants']

    #         if self.form.cleaned_data['languages']:
    #             expertForm.languages = self.form.cleaned_data['languages']

    #         if self.form.cleaned_data['method_of_introduction']:
    #             expertForm.method_of_introduction = self.form.cleaned_data['method_of_introduction']

    #         expertForm.has_industrial_research = request.POST.get('has_industrial_research')
    #         expertForm.number_of_researcher    = request.POST.get('number_of_researcher')

    #         # if expertForm.eq_test:
    #         #         eq_test = expertForm.eq_test
    #         # else:
    #         #     eq_test = EqTest()

    #         # eq_test.team_work              = request.POST.get('team_work', False)
    #         # eq_test.innovation             = request.POST.get('creative_thinking', False)
    #         # eq_test.devotion               = request.POST.get('sacrifice', False)
    #         # eq_test.productive_research    = request.POST.get('researching', False)
    #         # eq_test.national_commitment    = request.POST.get('obligation', False)
    #         # eq_test.collecting_information = request.POST.get('data_collection', False)
    #         # eq_test.business_thinking      = request.POST.get('morale', False)
    #         # eq_test.risk_averse            = request.POST.get('risk', False)
    #         # eq_test.save()

    #         photo = request.FILES.get('photo')
    #         if photo is not None:
    #             if os.path.isfile(expertForm.photo.path):
    #                 os.remove(expertForm.photo.path)
    #             expertForm.photo = photo

    #         expertForm.save()
    #         expert.status = "free"
    #         expert.save()
    #     return super().post(self, request, *args, **kwargs)


# class FUserInfo(generic.FormView):
#     template_name = 'expert/userInfo.html'
#     form_class = forms.ExpertInfoForm

#     def get(self, request, *args, **kwargs):
#         instance = get_object_or_404(ExpertForm, expert_user__user=request.user)
#         expert_info_form = forms.ExpertInfoForm(instance=instance)
#         scientific_instance = ScientificRecord.objects.filter(expert_form=instance)
#         executive_instance = ExecutiveRecord.objects.filter(expert_form=instance)
#         research_instance = ResearchRecord.objects.filter(expert_form=instance)
#         paper_instance = PaperRecord.objects.filter(expert_form=instance)
#         context = {'expert_info_form': expert_info_form,
#                    'keywords': instance.get_keywords(),
#                    'scientific_instance': scientific_instance,
#                    'executive_instance': executive_instance,
#                    'research_instance': research_instance,
#                    'paper_instance': paper_instance,
#                    'expert_form': instance,
#                    'scientific_form': forms.ScientificRecordForm(),
#                    'executive_form': forms.ExecutiveRecordForm(),
#                    'research_form': forms.ResearchRecordForm(),
#                    'paper_form': forms.PaperRecordForm()
#                    }
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         expertForm = get_object_or_404(ExpertForm, expert_user__user=request.user)
#         expert_info_form = forms.ExpertInfoForm(request.POST, request.FILES, instance=expertForm)
#         team_work = request.POST.get('team_work', False)
#         creative_thinking = request.POST.get('creative-thinking', False)
#         sacrifice = request.POST.get('sacrifice', False)
#         researching = request.POST.get('researching', False)
#         obligation = request.POST.get('obligation', False)
#         data_collection = request.POST.get('data-collection', False)
#         morale = request.POST.get('morale', False)
#         risk = request.POST.get('risk', False)
#         student_num = request.POST.get('student_num', False)
#         foreign_work = request.POST.get('foreign_work', False)
#         if expert_info_form.is_valid():
#             expert_form = expert_info_form.save(commit=False)
#             expert_form.expert_user = request.user.expertuser

#             if expertForm.eq_test:
#                 eq_test = expertForm.eq_test
#             else:
#                 eq_test = EqTest()
#             eq_test.team_work = team_work
#             eq_test.innovation = creative_thinking
#             eq_test.devotion = sacrifice
#             eq_test.productive_research = researching
#             eq_test.national_commitment = obligation
#             eq_test.collecting_information = data_collection
#             eq_test.business_thinking = morale
#             eq_test.risk_averse = risk
#             eq_test.save()
#             expert_form.eq_test = eq_test

#             if foreign_work and student_num:
#                 expert_form.has_industrial_research = foreign_work
#                 expert_form.number_of_researcher = student_num

#             keywords = expert_info_form.cleaned_data['keywords'].split(',')
#             keywords_list = []
#             for word in keywords:
#                 keywords_list.append(Keyword.objects.get_or_create(name=word)[0])
#             expert_form.keywords.set(keywords_list)

#             expert_form.save()
#             return HttpResponseRedirect(reverse('expert:index'))

#         return render(request, self.template_name, context)


@permission_required('expert.be_expert', login_url='/login/')
def scienfic_record_view(request):
    scientific_form = forms.ScientificRecordForm(request.POST)
    if scientific_form.is_valid():
        scientific_record = scientific_form.save(commit=False)
        scientific_record.expert_form = request.user.expertuser.expertform
        scientific_record.save()
        data = {
            'success': 'successful',
            'id': scientific_record.pk,
        }
        return JsonResponse(data)
    else:
        print('scientific_record form error occured')
        return JsonResponse(scientific_form.errors, status=400)


@permission_required('expert.be_expert', login_url='/login/')
def executive_record_view(request):
    executive_form = forms.ExecutiveRecordForm(request.POST)
    if executive_form.is_valid():
        executive_record = executive_form.save(commit=False)
        executive_record.expert_form = request.user.expertuser.expertform
        executive_record.save()
        data = {
            'success': 'successful',
            'id': executive_record.pk,
        }
        return JsonResponse(data)
    else:
        print('executive form error occured')
        return JsonResponse(executive_form.errors, status=400)


@permission_required('expert.be_expert', login_url='/login/')
def research_record_view(request):
    research_form = forms.ResearchRecordForm(request.POST)
    if research_form.is_valid():
        research_record = research_form.save(commit=False)
        research_record.expert_form = request.user.expertuser.expertform
        research_record.save()
        data = {
            'success': 'successful',
            'id': research_record.pk,
        }
        return JsonResponse(data)
    else:
        if 'status' in research_form.errors.keys():
            research_form.errors['status'] = "وضعیت نمی تواند خالی باشد."
        print('research record form error occured')
        return JsonResponse(research_form.errors, status=400)


@permission_required('expert.be_expert', login_url='/login/')
def paper_record_view(request):
    paper_form = forms.PaperRecordForm(request.POST)
    if paper_form.is_valid():
        paper_record = paper_form.save(commit=False)
        paper_record.expert_form = request.user.expertuser.expertform
        paper_record.save()
        data = {
            'success': 'successful',
            'id': paper_record.pk,
        }
        return JsonResponse(data)
    else:
        print('paper_record form error occured')
        return JsonResponse(paper_form.errors, status=400)


@permission_required('expert.be_expert', login_url='/login/')
def show_project_view(request):
    id = request.GET.get('id')
    project = Project.objects.get(id=id)
    data = {}
    if project.expert_accepted is not None:
        if project.expert_accepted.user == request.user:
            ActiveProjcet(request, project, data)
    return UsualShowProject(request, project, data)


def UsualShowProject(request, project, data):
    project_form = project.project_form
    if request.user.expertuser.status == "applied":
        data['applied'] = True
    else:
        data['applied'] = False
    if "status" not in data.keys():
        data["status"] = "non active"
        data['techniques_list'] = Technique.get_technique_list()
        comments = []        
        # comment_list = project.get_comments().exclude(industry_user=None).filter(expert_user=request.user.expertuser)
        # sys_comment = project.get_comments().filter(sender_type="system").filter(expert_user=request.user.expertuser)
        comment_list = project.get_comments().filter(expert_user=request.user.expertuser).filter(researcher_user=None)
        for comment in comment_list:
            try:
                url = comment.attachment.url
            except:
                url = "None"
            comments.append({
                'id': comment.id,
                'text': comment.description,
                'sender_type': comment.sender_type,
                'attachment': url,
                'pk': comment.pk,
            })
            if comment.sender_type in ["industry", "system"]:
                comment.status = "seen"
                comment.save()
        # for comment in sys_comment:
        #     comments.append({
        #         'id': comment.id,
        #         'text': comment.description,
        #         'sender_type': comment.sender_type,
        #         'pk': comment.pk,
        #     })
        #     if comment.sender_type == "system":
        #         comment.status = "seen"
        #         comment.save()
        data['comments'] = comments
    data['date'] = JalaliDate(project.date_submitted_by_industry).strftime("%Y/%m/%d")
    data['key_words'] = serializers.serialize('json', project_form.key_words.all())
    data['main_problem_and_importance'] = project_form.main_problem_and_importance
    data['progress_profitability'] = project_form.progress_profitability
    data['required_lab_equipment'] = project_form.required_lab_equipment
    data['approach'] = project_form.approach
    data['deadline'] = calculate_deadline(project.date_finished, project.date_submitted_by_industry)
    data['persian_title'] = project_form.persian_title
    data['english_title'] = project_form.english_title
    data['research_methodology'] = project_form.research_methodology
    data['policy'] = project_form.policy
    data['potential_problems'] = project_form.potential_problems
    data['required_budget'] = project_form.required_budget
    data['required_method'] = project_form.required_method
    data['project_phase'] = project_form.project_phase
    # data['predict_profit']= project_form.predict_profit 
    data['success'] = 'successful'
    # data['required_technique']=[]
    # for tech in project.project_form.required_technique:
    #     data['required_technique'].append(tech.__str__())
    return JsonResponse(data)


@permission_required('expert.be_expert', login_url='/login/')
def accept_project(request):
    expert_user = get_object_or_404(ExpertUser, user=request.user)
    project = Project.objects.get(id=request.POST.get('id'))
    project_form = project.project_form
    if expert_user in project.expert_applied.all():
        return JsonResponse({
            'message': 'درخواست شما قبلا هم ارسال شده است',
        }, status=400)
    else:
        technique_list = request.POST.getlist('technique')
        if len(technique_list) == 0:
            return JsonResponse({
                'message': 'متاسفانه بدون انتخاب تکنیک‌های موردنظر، امکان ارسال درخواست وجود ندارد.',
            }, status=400)
        expert_request = ExpertRequestedProject.objects.create(expert=expert_user, project=project)
        for technique in technique_list:
            project_technique = Technique.objects.get_or_create(technique_title=technique[:-2])
            expert_request.required_technique.add(project_technique[0])
        expert_request.save()
        expert_user.status = "applied"
        expert_user.save()
        text = "درخواست شما برای صنعت ارسال شد."
        comment = Comment(description=text,
                          sender_type="system",
                          project=project,
                          expert_user=expert_user,
                          status='unseen')
        comment.save()
        try:
            subjectForAdmin = "درخواست قرار ملاقات"
            messageForAdmin = """با سلام و احترام\n
            استاد {} برای پروژه {} از مرکز {} در خواست قرار ملاقات بابت عقد قراداد داده است. خواهشمندم در اسرع وقت پیگیری نمایید.\n
            با تشکر
            """.format(str(expert_user.expertform), str(project), str(project.industry_creator.profile))
            send_mail(
                subject=subjectForAdmin,
                message=messageForAdmin,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER, "sepehr.metanat@gmail.com"],
                fail_silently=False
            )
            # html_templateForAdmin = get_template('registration/projectRequest_template.html')
            # email_templateForAdmin = html_templateForAdmin.render({'message': messageForAdmin})
            # msgForAdmin = EmailMultiAlternatives(subject=subjectForAdmin, from_email=settings.EMAIL_HOST_USER,
            #                                      to=[settings.EMAIL_HOST_USER, ])
            # msgForAdmin.attach_alternative(email_templateForAdmin, 'text/html')
            # msgForAdmin.send()

            subjectForExpert = "درخواست قرار ملاقات"
            messageForExpert = """با سلام و احترام\n
            درخواست قرار ملاقات شما برای پروژه {} برای ادمین ارسال شد.\n
            با تشکر
            """.format(str(project))
            html_templateForAdmin = get_template('registration/projectRequest_template.html')
            email_templateForAdmin = html_templateForAdmin.render({'message': messageForExpert})
            msgForExpert = EmailMultiAlternatives(subject=subjectForExpert, from_email=settings.EMAIL_HOST_USER,
                                                  to=[request.user.get_username(), ])
            msgForExpert.attach_alternative(email_templateForAdmin, 'text/html')
            msgForExpert.send()
        except TimeoutError:
            print("Timeout Occure.")
        return JsonResponse({
            'message': 'درخواست شما با موفقیت ثبت شد. لطفا تا بررسی توسط صنعت مربوطه، منتظر بمانید.'
        })


@permission_required('expert.be_expert', login_url='/login/')
def add_research_question(request):
    research_question_form = forms.ResearchQuestionForm(request.POST, request.FILES)
    if research_question_form.is_valid():
        data = {'success': 'successful'}
        research_question = research_question_form.save(commit=False)
        research_question.expert = request.user.expertuser
        if request.FILES.get('attachment'):
            attachment = request.FILES.get('attachment')
            research_question.attachment.save(attachment.name, attachment)
        research_question.save()
        data["id"] = research_question.id
        return JsonResponse(data)
    else:
        return JsonResponse(research_question_form.errors, status=400)


@permission_required('expert.be_expert', login_url='/login/')
def show_research_question(request):
    try:
        research_question = ResearchQuestion.objects.get(id=request.GET.get('id'))
    except:
        return JsonResponse(data={}, status=400)

    answers_list = []
    for answer in research_question.get_answers():
        researcherProfile = ResearcherProfile.objects.get(researcher_user=answer.researcher)
        domain = answer.researcher.user.get_username().split("@")[-1]
        file_name = answer.answer.name.split(domain)[-1][1:]
        answer_json = {
            'researcher_name': researcherProfile.__str__(),
            'hand_out_date': JalaliDate(answer.hand_out_date).strftime("%Y/%m/%d"),
            'is_correct': answer.is_correct,
            'file_name': file_name,
            'answer_attachment': answer.answer.url,
            'answer_id': str(answer.id),
        }
        answers_list.append(answer_json)

    json_response = {
        'question_status': research_question.status,
        'question_date': JalaliDate(research_question.submitted_date).strftime("%Y/%m/%d"),
        'question_body': research_question.question_text,
        'question_title': research_question.question_title,
        'question_answers_list': answers_list,
    }
    if research_question.attachment:
        attachment = research_question.attachment
        json_response['question_attachment_path'] = attachment.url
        json_response['question_attachment_name'] = attachment.name.split('/')[-1]
        json_response['question_attachment_type'] = attachment.name.split('/')[-1].split('.')[-1]
    return JsonResponse(json_response)


@permission_required('expert.be_expert', login_url='/login/')
def terminate_research_question(request):
    research_question = ResearchQuestion.objects.filter(id=request.GET.get('id')).first()
    research_question.status = 'answered'
    research_question.save(update_fields=['status'])
    return JsonResponse({
        'success': 'successful'
    })


@permission_required('expert.be_expert', login_url='/login/')
def set_answer_situation(request):
    answer = ResearchQuestionInstance.objects.filter(id=request.GET.get('id')).first()
    title = ""
    text = ""
    messageType = 0
    if request.GET.get('type') == 'true':
        answer.is_correct = 'correct'
        title = "تایید سوال پژوهشی"
        text = """با سلام،
پژوهشگر گرامی، پاسخ سوال پژوهشی شما پذیرفته شد.
به این ترتیب، پیوستن شما به مجموعه پژوهشگران «چمران‌تیم» را تبریک می‌گوییم و امیدواریم شاهد پیشرفت شما در زمینه پژوهش باشیم.
از این پس می‌توانید از طریق قسمت «پروژه‌ها» برای شرکت در پروژه‌های تعریف‌شده توسط مجموعه‌های پژوهشی، درخواست ارسال کنید. 
البته در نظر داشته باشید که برای شرکت در هر پروژه‌ای، لازم است مهارت‌های پژوهشی آن پروژه را قبلا کسب کرده باشید. به همین خاطر، توصیه می‌کنیم به قسمت «مهارت‌های پژوهشی» حساب کاربری‌تان هم سر بزنید و با افزایش تعداد مهارت‌های‌تان، شانس خود را برای شرکت در پروژه‌ها افزایش دهید.
همچنین، با تکمیل یا بارگذاری رزومه علمی‌تان از طریق قسمت «اطلاعات کاربری»، می‌توانید توانمندی‌های خود را در هنگام انتخاب شدن‌تان توسط استاد و یا مجموعه پژوهشی، نشان دهید.
با آرزوی موفقیت، 
چمران‌تیم"""
        messageType = 0
    else:
        answer.is_correct = 'wrong'
        title = "رد سوال پژوهشی"
        text = """با سلام،
پژوهشگر گرامی، متاسفانه پاسخ شما به سوال پژوهشی (در مهلت یک هفته‌ای ارسال نشد / به دلیل نداشتن کیفیت مناسب، مورد قبول واقع نشد).
علی‌رغم میل درونی، حساب کاربری شما به مدت دو هفته به حالت تعلیق در خواهد آمد و پس از آن، مجددا می‌توانید در یک سوال پژوهشی شرکت نمایید.
امیدواریم دو هفته‌ی دیگر هم شما را ببینیم.
در ضمن، در صورتی که فکر می‌کنید این پیام به اشتباه ارسال شده است، می‌توانید مراتب اعتراض خود را از طریق شماره تلفن ۰۹۱۰۲۱۴۳۴۵۱ و یا فرم ارسال گزارش (با کلیک بر روی تصویر علامت تعجب در گوشه بالا سمت چپ صفحه نمایش) ارسال فرمایید.
با آرزوی موفقیت،
چمران‌تیم"""
        messageType = 1
    try:
        message = Message.objects.filter(title=title).first()
    except:
        message = None
    if message is None:
        message = Message(title=title,
                          text=text,
                          type=messageType)
        message.save()
    message.receiver.add(answer.researcher.user)
    message.save()
    html_templateForAdmin = get_template('registration/projectRequest_template.html')
    email_templateForAdmin = html_templateForAdmin.render({'message': text})
    email = EmailMultiAlternatives(subject=title, from_email=settings.EMAIL_HOST_USER,
                                   to=[answer.researcher.user.get_username(), ])
    email.attach_alternative(email_templateForAdmin, 'text/html')
    email.send()
    answer.save(update_fields=['is_correct'])
    return JsonResponse({
        'success': 'successful'
    })


# @permission_required('expert.be_expert', login_url='/login/')
# def show_researcher_preview(request):
#     researcherProfile = ResearcherProfile.objects.get(id=request.GET.get('id'))
#     researcher = researcherProfile.researcher_user
#     researcher_information = {
#         'photo': researcherProfile.photo.url,
#         'name': researcherProfile.__str__(),
#         'major': researcherProfile.major,
#         'grade': researcherProfile.grade,
#         'university': researcherProfile.university,
#         'entry_year': researcherProfile.entry_year,
#         'resume'    : researcherProfile.resume.url,
#         'techniques': [],
#         'scientific_record': serializers.serialize('json', ResearcherScientificRecord.objects.filter(
#             researcherProfile=researcherProfile)),
#         'executive_record': serializers.serialize('json', ResearcherExecutiveRecord.objects.filter(
#             researcherProfile=researcherProfile)),
#         'research_record': serializers.serialize('json', StudiousRecord.objects.filter(researcherProfile=researcherProfile)),
#     }
#     for tech in TechniqueInstance.objects.filter(researcher=researcher):
#         researcher_information['techniques'].append(tech.technique.technique_title)
#     project = get_object_or_404(Project ,pk=request.GET["project_id"])
#     comments = []
#     comment_list = project.comment_set.all().filter(researcher_user=researcher).exclude(sender_type='system')
#     for comment in comment_list:
#         try:
#             url = comment.attachment.url)
#         except:
#             url = "None"
#         comments.append({
#             'id': comment.id,
#             'text': comment.description,
#             'sender_type': comment.sender_type,
#             'attachment' : url,
#             'pk' : comment.pk,
#         })
#         if comment.sender_type == 'researcher':
#             comment.status = 'seen'
#             comment.save()
#     researcher_information['comments'] = comments
#     return JsonResponse(researcher_information)

@permission_required('expert.be_expert', login_url='/login/')
def CommentForResearcher(request):
    form = forms.CommentForm(request.POST, request.FILES)
    project = Project.objects.get(pk=request.POST['project_id'])
    researcherProfile = ResearcherProfile.objects.get(pk=request.POST['researcher_id'])
    researcher = researcherProfile.researcher_user
    if form.is_valid():
        description = form.cleaned_data['description']
        attachment = form.cleaned_data['attachment']
        comment = Comment(description=description
                          , attachment=attachment
                          , project=project
                          , researcher_user=researcher
                          , expert_user=request.user.expertuser
                          , sender_type="expert"
                          , status='unseen')
        comment.save()
        if form.cleaned_data["attachment"] is not None:
            data = {
                'success': 'successful',
                'pk': comment.pk,
                'attachment': comment.attachment.url.split("/")[-1],
                'description': comment.description,
            }
        else:
            data = {
                'success': 'successful',
                'pk': comment.pk,
                'description': comment.description,
                'attachment': "None",
            }
        return JsonResponse(data)
    return JsonResponse(form.errors, status=400)


@permission_required('expert.be_expert', login_url='/login/')
def CommentForIndustry(request):
    project = Project.objects.get(id=request.POST['project_id'])
    form = forms.CommentForm(request.POST, request.FILES)
    if form.is_valid():
        if not project.expert_messaged.filter(id=request.user.expertuser.id).exists():
            project.expert_messaged.add(ExpertUser.objects.all().filter(id=request.user.expertuser.id).first())
            project.save()
        new_comment = Comment.objects.create(sender_type="expert",
                                             project=project,
                                             expert_user=request.user.expertuser,
                                             industry_user=project.industry_creator,
                                             description=form.cleaned_data["description"],
                                             attachment=form.cleaned_data["attachment"],
                                             status='unseen')
        new_comment.save()
        if form.cleaned_data["attachment"] is not None:
            data = {
                'success': 'successful',
                'pk': new_comment.pk,
                'attachment': new_comment.attachment.url.split("/")[-1],
                'description': new_comment.description,
            }
        else:
            data = {
                'success': 'successful',
                'pk': new_comment.pk,
                'description': new_comment.description,
                'attachment': "None",
            }
        return JsonResponse(data=data)
    else:
        return JsonResponse(form.errors, status=400)


@permission_required([], login_url='/login/')
def ShowTechnique(request):
    TYPE = (
        'molecular_biology',
        'immunology',
        'imaging',
        'histology',
        'general_lab',
        'animal_lab',
        'lab_safety',
        'biochemistry',
        'cellular_biology',
        'research_methodology',
    )
    query = []
    for tp in TYPE:
        query.append(list(Technique.objects.filter(technique_type=tp).values_list('technique_title', flat=True)))
        query[-1].append(tp)
    data = {}
    for q in query:
        if len(q) > 1:
            data[q[-1]] = q[:-1]
    return JsonResponse(data=data)


@permission_required([], login_url='/login/')
def GetResume(request):
    expert_id = request.GET['id']
    expert = get_object_or_404(ExpertUser, pk=expert_id)
    expert_form = get_object_or_404(ExpertForm, expert_user=expert)
    if expert_form.scientific_rank == 1:
        scientific_rank = 'مربی'
    elif expert_form.scientific_rank == 2:
        scientific_rank = 'استادیار'
    elif expert_form.scientific_rank == 3:
        scientific_rank = 'دانشیار'
    elif expert_form.scientific_rank == 4:
        scientific_rank = 'استاد'
    elif expert_form.scientific_rank == 5:
        scientific_rank = 'استاد تمام'
    elif expert_form.scientific_rank == 6:
        scientific_rank = 'پژوهشگر'
    data = {
        'name': expert_form.fullname,
        'photo': expert_form.photo.url,
        "university": expert_form.university,
        "scientific_rank": scientific_rank,
        "special_field": expert_form.special_field,
        'exe_record': serializers.serialize('json', ExecutiveRecord.objects.filter(
            expert_form=expert_form)),

        'research_record': serializers.serialize('json', ResearchRecord.objects.filter(
            expert_form=expert_form)),

        'sci_record': serializers.serialize('json', ScientificRecord.objects.filter(
            expert_form=expert_form)),

        'paper_record': serializers.serialize('json', PaperRecord.objects.filter(
            expert_form=expert_form)),

        "awards": expert_form.awards,
        'languages': expert_form.languages,
    }
    if expert_form.resume:
        data['resume'] = expert_form.resume.url

    if expert_form.has_industrial_research == 'yes':
        data['has_industrial_research'] = 'داشته'
    if expert_form.has_industrial_research == 'no':
        data['has_industrial_research'] = 'نداشته'

    if expert_form.number_of_researcher == 1:
        data['researcher_count'] = '1-10'
    if expert_form.number_of_researcher == 2:
        data['researcher_count'] = '11-30'
    if expert_form.number_of_researcher == 3:
        data['researcher_count'] = '31-60'
    if expert_form.number_of_researcher == 4:
        data['researcher_count'] = '+60'

    return JsonResponse(data=data)


@permission_required('expert.be_expert', login_url='/login/')
def confirmResearcher(request):
    try:
        researcher = get_object_or_404(ResearcherUser, pk=request.POST['researcher_id'])
        project = get_object_or_404(Project, pk=request.POST['project_id'])
        project.researcher_accepted.add(researcher)
        researcher.status.status = 'involved'
        project.save()
        researcher.status.save()
        return JsonResponse(data={})
    except:
        return JsonResponse(data={}, status=400)


@permission_required('expert.be_expert', login_url='/login/')
def refuseResearcher(request):
    try:
        researcher = get_object_or_404(ResearcherUser, pk=request.POST['researcher_id'])
        project = get_object_or_404(Project, pk=request.POST['project_id'])
        project.researcher_accepted.remove(researcher)
        project.researcher_banned.add(researcher)
        project.save()
        return JsonResponse(data={})
    except:
        return JsonResponse(data={}, status=400)


def ActiveProjcet(request, project, data):
    industryform = project.industry_creator.profile
    projectDate = [
        gregorian_to_numeric_jalali(project.date_start),
        gregorian_to_numeric_jalali(project.date_project_started),
        gregorian_to_numeric_jalali(project.date_phase_two_deadline),
        gregorian_to_numeric_jalali(project.date_phase_three_deadline),
        gregorian_to_numeric_jalali(project.date_finished),
    ]
    # data = {
    data["status"] = "active"
    data["industry_name"] = industryform.name
    data["industry_logo"] = industryform.photo.url
    data['enforcer_name'] = str(project.expert_accepted.expertform)
    data["executive_info"] = project.executive_info
    data["budget_amount"] = project.project_form.required_budget
    data['timeScheduling'] = projectDate
    data["techniques"] = []
    # }
    projectRequest = ExpertRequestedProject.objects.filter(project=project).filter(
        expert=project.expert_accepted).first()
    for technique in projectRequest.required_technique.all():
        data["techniques"].append(technique.__str__())
    try:
        researcher_request = RequestResearcher.objects.get(project=project)
        if researcher_request.need_researcher != 0:
            data['request_status'] = True
        else:
            data['request_status'] = False
    except:
        data['request_status'] = True
    expert = project.expert_accepted
    # all_researchers = Comment.objects.filter(project=project).filter(expert_user=expert).filter(sender_type="researcher").values('researcher_user').distinct()
    # data['researcher_comment'] = []    
    # for researcher in all_researchers:
    #     researcherInfo = {
    #         'id'   : researcher['researcher_user'],
    #         "name" : str(ResearcherProfile.objects.get(researcher_user=researcher['researcher_user'])),
    #     }
    #     data['researcher_comment'].append(researcherInfo)

    data['researcher_accepted'] = []
    for researcher in project.researcher_accepted.all():
        researcherInfo = {
            'id': researcher.pk,
            "name": str(researcher.researcherprofile),
            "profile": researcher.researcherprofile.photo,
        }
        data['researcher_accepted'].append(researcherInfo)
    return JsonResponse(data=data)


@permission_required('expert.be_expert', login_url='/login/')
def DeleteScientificRecord(request):
    try:
        sci_rec = get_object_or_404(ScientificRecord, pk=request.POST['pk'])
    except:
        return JsonResponse({"errors": "Scientific record isn't found"}, status=400)
    sci_rec.delete()
    return JsonResponse({"successfull": "Scientific record is deleted"})


@permission_required('expert.be_expert', login_url='/login/')
def DeleteExecutiveRecord(request):
    try:
        exe_rec = get_object_or_404(ExecutiveRecord, pk=request.POST['pk'])
    except:
        return JsonResponse({"errors": "Executive record isn't found"}, status=400)
    exe_rec.delete()
    return JsonResponse({"successfull": "Executive record is deleted"})


@permission_required('expert.be_expert', login_url='/login/')
def DeleteResearchRecord(request):
    try:
        research_rec = get_object_or_404(ResearchRecord, pk=request.POST['pk'])
    except:
        return JsonResponse({"errors": "Research Record isn't found"}, status=400)
    research_rec.delete()
    return JsonResponse({"successfull": "Research Record is deleted"})


@permission_required('expert.be_expert', login_url='/login/')
def DeletePaperRecord(request):
    try:
        paper_rec = get_object_or_404(PaperRecord, pk=request.POST['pk'])
    except:
        return JsonResponse({"errors": "Paper Record isn't found"}, status=400)
    paper_rec.delete()
    return JsonResponse({"successfull": "Paper Record is deleted"})


@permission_required('expert.be_expert', login_url='/login/')
def ExpertRequestResearcher(request):
    project = Project.objects.get(id=request.POST['project_id'])
    form = forms.RequestResearcherForm(request.POST)
    if form.is_valid():
        expert = request.user.expertuser
        least_hour = form.cleaned_data['least_hour']
        researcher_count = form.cleaned_data['researcher_count']
        try:
            researcher_request = RequestResearcher.objects.get(project=project)
            researcher_request.researcher_count += researcher_count
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


@permission_required('expert.be_expert', login_url='/login/')
def GetResearcherComment(request):
    project_id = request.GET['project_id']
    researcher_id = request.GET['researcher_id']
    comments = Comment.objects.filter(project=project_id).filter(researcher_user=researcher_id).exclude(
        sender_type="system")
    data = {'comments': []}
    for comment in comments:
        try:
            url = comment.attachment.url
        except:
            url = "None"
        commentInfo = {
            'id': comment.id,
            'text': comment.description,
            'sender_type': comment.sender_type,
            'attachment': url,
        }
        if comment.sender_type == "researcher":
            comment.status = "seen"
            comment.save()
        data['comments'].append(commentInfo)

    return JsonResponse(data=data)

@permission_required('expert.be_expert', login_url='/login/')
def checkUserId(request):
    if request.is_ajax() and request.method == "POST":
        user_id = request.POST.get("user_id")
        if not bool(USER_ID_PATTERN.match(user_id)):
            return JsonResponse({"invalid_input": True})
        if user_id != request.user.expertuser.userId:
            if ExpertUser.objects.filter(userId=user_id).count():
                return JsonResponse({"is_unique": False, "invalid_input": False})
        return JsonResponse({"is_unique": True, "invalid_input": False})


@permission_required('expert.be_expert', login_url='/login/')
def CollectData(request):
    if not TempExpertForm.objects.filter(expertUser=request.user.expertuser).count():
        link = request.POST['link']
        # link = "https://isid.research.ac.ir/Reza_Malekzadeh"
        try:
            collectedData = webScraping.webScraping(link=link)
        except:
            return JsonResponse(data={}, status=400)
        scientific_rank = ""
        special_field = ""
        if "پژوهشگر" in collectedData['information'][0]:
            scientific_rank = 6
            special_field = collectedData['information'][0][8:]
        elif "استاد ممتاز" in collectedData['information'][0]:
            scientific_rank = 5
            special_field = collectedData['information'][0][12:]
        elif "استادیار" in collectedData['information'][0]:
            scientific_rank = 2
            special_field = collectedData['information'][0][9:]
        elif "استاد" in collectedData['information'][0]:
            scientific_rank = 4
            special_field = collectedData['information'][0][6:]
        elif "دانشیار" in collectedData['information'][0]:
            scientific_rank = 3
            special_field = collectedData['information'][0][8:]
        elif "مربی" in collectedData['information'][0]:
            scientific_rank = 1
            special_field = collectedData['information'][0][5:]
        TempExpertForm
        tempForm = TempExpertForm(expertUser=request.user.expertuser,
                                fullname=collectedData['fullname'],
                                special_field=special_field,
                                scientific_rank=scientific_rank,
                                university=collectedData['information'][-1]
                                )
        tempForm.save()
        tempForm.photo.save(str(request.user.expertuser) + "_photo.jpg", collectedData['photo'])
        for keyword in collectedData['keywords']:
            tempForm.keywords.add(Keyword.objects.get_or_create(name=keyword)[0])

        for paper in collectedData['papers_information']:
            temp = TempPaperRecord(tempExpertForm=tempForm,
                                research_title=paper['title'],
                                date_published=paper['publish_year'],
                                published_at=paper['source'],
                                impact_factor=paper['impact_factor'],
                                citation=paper['citation'])
            temp.save()
        keywords = collectedData['keywords']
        papers_information = collectedData['papers_information']
    else:
        tempForm = TempExpertForm.objects.get(expertUser=request.user.expertuser)
        keywords = [keyword.name for keyword in tempForm.keywords.all()]
        papers_information = [model_to_dict(paper) for paper in tempForm.temppaperrecord_set.all()]

    data = {
        "photo": tempForm.photo.url,
        "fullname": tempForm.fullname,
        "scientific_rank": tempForm.scientific_rank,
        "special_field": tempForm.special_field,
        "university": tempForm.university,
        "keywords": keywords,
        "papers": papers_information,
    }
    return JsonResponse(data=data)


def submitData(request):
    expert_user = request.user.expertuser
    tempExpertForm = get_object_or_404(TempExpertForm, expertUser=expert_user)
    expertForm = ExpertForm(expert_user=expert_user,
                            photo=tempExpertForm.photo,
                            special_field=tempExpertForm.special_field,
                            scientific_rank=tempExpertForm.scientific_rank,
                            university=tempExpertForm.university, )
    expertForm.save()
    for keyword in tempExpertForm.keywords.all():
        expertForm.keywords.add(keyword)
    expertForm.save()
    tempPapers = TempPaperRecord.objects.filter(tempExpertForm=tempExpertForm)
    for tempPaper in tempPapers:
        paper = PaperRecord(expert_form=expertForm,
                            research_title=tempPaper.research_title,
                            date_published=tempPaper.date_published,
                            published_at=tempPaper.published_at,
                            impact_factor=tempPaper.impact_factor,
                            citation=tempPaper.citation,
                            )
        paper.save()
    tempExpertForm.delete()
    return JsonResponse(data={})


def ActiveProject(request, project, data):
    data['accepted'] = True
    data['project_pk'] = project.id
    industryform = project.industry_creator.profile
    data['projectForm'] = model_to_dict(project.project_form)
    projectDate = {
        "start": gregorian_to_numeric_jalali(project.date_start),
        "firstPhase": gregorian_to_numeric_jalali(project.date_project_started),
        "secondPhase": gregorian_to_numeric_jalali(project.date_phase_two_deadline),
        "thirdPhase": gregorian_to_numeric_jalali(project.date_phase_three_deadline),
        "finished": gregorian_to_numeric_jalali(project.date_finished),
    }
    data['timeScheduling'] = projectDate
    data['title'] = project.project_form.persian_title
    data["industry_name"] = industryform.name
    if industryform.photo:
        data["industry_logo"] = industryform.photo.url
    data['enforcer_name'] = str(project.expert_accepted.expertform)
    data['enforcer_id'] = project.expert_accepted.pk
    data["executive_info"] = project.executive_info
    data["budget_amount"] = project.project_form.required_budget

    data['comments'] = []
    for comment in project.get_comments().exclude(industry_user=None).filter(expert_user=project.expert_accepted):
        try:
            # TODO
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
        if comment.sender_type == "industry" or comment.sender_type == "system":
            comment.status = "seen"
            comment.save()
    data['deadline'] = 'نا مشخص'
    data['submission_date'] = gregorian_to_numeric_jalali(project.date_submitted_by_industry)
    evaluation_history = project.expert_accepted.industryevaluateexpert_set.filter(project=project)
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


class show_active_project(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = "expert/project.html"
    permission_required = ('expert.be_expert',)
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, code=kwargs["code"])
        if project.expert_accepted.user != request.user:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, code=kwargs["code"])
        context = ActiveProject(request=self.request, project=project, data=context)
        context['requestResearcherForm'] = forms.RequestResearcherForm()
        context['researcher_accepted'] = []
        for researcher in project.researcher_accepted.all():
            researcher = {
                "id": researcher.pk,
                "fullname": researcher.researcherprofile.fullname,
                "photo": researcher.researcherprofile.photo
            }
            context['researcher_accepted'].append(researcher)
        if project.researcher_accepted.all():
            context['researcherComment'] = project.get_comments().exclude(researcher_user=project.researcher_accepted.all()[0]).exclude(expert_user=None)
        return context
