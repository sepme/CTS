from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, get_object_or_404, Http404
from .models import ExpertForm, EqTest, ExpertUser
from .forms import *
from industry.models import Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, QueryDict
from persiantools.jdatetime import JalaliDate
from datetime import datetime
from django.core import serializers
import json
from industry.models import *
from researcher.models import ScientificRecord as ResearcherScientificRecord
from researcher.models import ExecutiveRecord as ResearcherExecutiveRecord
from researcher.models import ResearcherProfile, Technique, StudiousRecord ,TechniqueInstance


def calculate_deadline(finished, started):
    try:
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
    except:
        return 'تاریخ نامشخص'


class Index(generic.TemplateView):
    template_name = 'expert/index.html'


class ResearcherRequest(generic.TemplateView):
    template_name = 'expert/researcherRequest.html'

    def get(self, request, *args, **kwargs):
        expert_user = get_object_or_404(ExpertUser, user=request.user)
        projects_list = Project.objects.filter(expert_accepted=expert_user).only('project_form__project_title_persian')
        projects_data = []
        for project in projects_list:
            try:
                researchers_applied = []
                researchers_form = [ResearcherProfile.objects.filter(researcher_user=researcher_user)[0] for researcher_user in project.researcher_applied.all()]
                if len(researchers_form) == 0:
                    continue
                for research in researchers_form:
                    try:
                        techniques = [tech.technique.technique_title for tech in TechniqueInstance.objects.filter(researcher=research.researcher_user)]
                        researcher_applied = {
                            'profile': research,
                            'techniques' : techniques,
                        }
                        researchers_applied.append(researcher_applied)
                    except:
                        continue
                appending = {
                    'project': project.project_form.project_title_persian,
                    "researchers_applied" : researchers_applied
                }
                projects_data.append(appending)
            except:
                continue                

        context = {}
        if len(projects_data) != 0:
            context = {'applications': projects_data}
        print(context)

        return render(request, self.template_name, context)


class Messages(generic.TemplateView):
    template_name = 'expert/messages.html'


class Questions(generic.TemplateView):
    template_name = 'expert/questions.html'

    def get(self, request, *args, **kwargs):
        expert_user = request.user.expertuser
        research_questions = ResearchQuestion.objects.filter(expert=expert_user)
        context = {
            'research_question_form': ResearchQuestionForm(),
            'research_questions': research_questions,
        }
        return render(request, self.template_name, context)


@login_required(login_url='/login/')
def index(request):
    expert_user = get_object_or_404(ExpertUser, user=request.user)
    if request.method == 'POST':
        form = InitialInfoForm(request.POST, request.FILES)
        print(form.is_valid())

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            special_field = form.cleaned_data['special_field']
            melli_code = form.cleaned_data['melli_code']
            scientific_rank = form.cleaned_data['scientific_rank']
            university = form.cleaned_data['university']
            address = form.cleaned_data['address']
            home_number = form.cleaned_data['home_number']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email_address']
            expert_form = ExpertForm.objects.create(expert_firstname=first_name, expert_lastname=last_name,
                                                    special_field=special_field, national_code=melli_code,
                                                    scientific_rank=scientific_rank, university=university,
                                                    phone_number=home_number, home_address=address,
                                                    mobile_phone=phone_number, email_address=email)
            expert_form.expert_user = expert_user
            if request.FILES.get('photo'):
                photo = request.FILES.get('photo')
                expert_form.photo.save(photo.name, photo)
            expert_user.status = 'free'
            expert_user.save()
            expert_form.save()
            return HttpResponseRedirect(reverse('expert:index'))
        else:
            print(form.errors)
    form = InitialInfoForm()
    projects = Project.objects.all()
    return render(request, 'expert/index.html', {'form': form,
                                                 'expert_user': expert_user,
                                                 'projects': projects})


class UserInfo(generic.FormView):
    template_name = 'expert/userInfo.html'
    form_class = ExpertInfoForm

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(ExpertForm, expert_user__user=request.user)
        expert_info_form = ExpertInfoForm(instance=instance)
        scientific_instance = ScientificRecord.objects.filter(expert_form=instance)
        executive_instance = ExecutiveRecord.objects.filter(expert_form=instance)
        research_instance = ResearchRecord.objects.filter(expert_form=instance)
        paper_instance = PaperRecord.objects.filter(expert_form=instance)
        context = {'expert_info_form': expert_info_form,
                   'keywords': instance.get_keywords(),
                   'scientific_instance': scientific_instance,
                   'executive_instance': executive_instance,
                   'research_instance': research_instance,
                   'paper_instance': paper_instance,
                   'expert_form': instance,
                   'scientific_form': ScientificRecordForm(),
                   'executive_form': ExecutiveRecordForm(),
                   'research_form': ResearchRecordForm(),
                   'paper_form': PaperRecordForm()
                   }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        instance = get_object_or_404(ExpertForm, expert_user__user=request.user)
        expert_info_form = ExpertInfoForm(request.POST, request.FILES, instance=instance)
        team_work = request.POST.get('team_work', False)
        creative_thinking = request.POST.get('creative-thinking', False)
        sacrifice = request.POST.get('sacrifice', False)
        researching = request.POST.get('researching', False)
        obligation = request.POST.get('obligation', False)
        data_collection = request.POST.get('data-collection', False)
        morale = request.POST.get('morale', False)
        risk = request.POST.get('risk', False)
        student_num = request.POST.get('student_num', False)
        foreign_work = request.POST.get('foreign_work', False)
        scientific_instance = ScientificRecord.objects.filter(expert_form=instance)
        executive_instance = ExecutiveRecord.objects.filter(expert_form=instance)
        research_instance = ResearchRecord.objects.filter(expert_form=instance)
        paper_instance = PaperRecord.objects.filter(expert_form=instance)
        context = {'expert_info_form': expert_info_form,
                   'scientific_instance': scientific_instance,
                   'executive_instance': executive_instance,
                   'research_instance': research_instance,
                   'paper_instance': paper_instance,
                   'expert_form': instance,
                   'scientific_form': ScientificRecordForm(),
                   'executive_form': ExecutiveRecordForm(),
                   'research_form': ResearchRecordForm(),
                   'paper_form': PaperRecordForm()
                   }
        if expert_info_form.is_valid():
            expert_form = expert_info_form.save(commit=False)
            expert_form.expert_user = request.user.expertuser

            if team_work and creative_thinking and sacrifice and researching and obligation and data_collection and morale and risk:
                if instance.eq_test:
                    eq_test = instance.eq_test
                else:
                    eq_test = EqTest()
                eq_test.team_work = team_work
                eq_test.innovation = creative_thinking
                eq_test.devotion = sacrifice
                eq_test.productive_research = researching
                eq_test.national_commitment = obligation
                eq_test.collecting_information = data_collection
                eq_test.business_thinking = morale
                eq_test.risk_averse = risk
                eq_test.save()
                expert_form.eq_test = eq_test

            if foreign_work and student_num:
                expert_form.has_industrial_research = foreign_work
                expert_form.number_of_researcher = student_num

            if request.FILES.get('photo'):
                photo = request.FILES.get('photo')
                expert_form.photo.save(photo.name, photo)

            keywords = expert_info_form.cleaned_data['keywords'].split(',')
            keywords_list = []
            for word in keywords:
                keywords_list.append(Keyword.objects.get_or_create(name=word)[0])
            expert_form.keywords.set(keywords_list)

            expert_form.save()
            return HttpResponseRedirect(reverse('expert:index'))

        return render(request, self.template_name, context)


def scienfic_record_view(request):
    print(request.is_ajax())
    # form = request.GET.get('formData', None)
    # print(form)
    print(request.POST)
    scientific_form = ScientificRecordForm(request.POST)
    if scientific_form.is_valid():
        print(scientific_form.cleaned_data)
        data = {'success': 'successful'}
        scientific_record = scientific_form.save(commit=False)
        scientific_record.expert_form = request.user.expertuser.expertform
        scientific_record.save()
        return JsonResponse(data)
    else:
        print('form error occured')
        return JsonResponse(scientific_form.errors, status=400)


def executive_record_view(request):
    executive_form = ExecutiveRecordForm(request.POST)
    if executive_form.is_valid():
        print(executive_form.cleaned_data)
        data = {'success': 'successful'}
        executive_record = executive_form.save(commit=False)
        executive_record.expert_form = request.user.expertuser.expertform
        executive_record.save()
        return JsonResponse(data)
    else:
        print('form error occured')
        return JsonResponse(executive_form.errors, status=400)


def research_record_view(request):
    research_form = ResearchRecordForm(request.POST)
    if research_form.is_valid():
        print(research_form.cleaned_data)
        data = {'success': 'successful'}
        research_record = research_form.save(commit=False)
        research_record.expert_form = request.user.expertuser.expertform
        research_record.save()
        return JsonResponse(data)
    else:
        print('form error occured')
        return JsonResponse(research_form.errors, status=400)


def paper_record_view(request):
    paper_form = PaperRecordForm(request.POST)
    if paper_form.is_valid():
        print(paper_form.cleaned_data)
        data = {'success': 'successful'}
        paper_record = paper_form.save(commit=False)
        paper_record.expert_form = request.user.expertuser.expertform
        paper_record.save()
        return JsonResponse(data)
    else:
        print('form error occured')
        return JsonResponse(paper_form.errors, status=400)


def show_project_view(request):
    expert_user = request.user.expertuser
    id = request.GET.get('id')
    project = Project.objects.get(id=id)
    project_form = project.project_form
    data = {
        'date': JalaliDate(project.date_submitted_by_industry).strftime("%Y/%m/%d"),
        'key_words': serializers.serialize('json', project_form.key_words.all()),
        'main_problem_and_importance': project_form.main_problem_and_importance,
        'progress_profitability': project_form.progress_profitability,
        'required_lab_equipment': project_form.required_lab_equipment,
        'approach': project_form.approach,
        'deadline': calculate_deadline(project.date_finished, project.date_submitted_by_industry),
        'project_title_persian': project_form.project_title_persian,
        'project_title_english': project_form.project_title_english,
        'research_methodology': project_form.research_methodology,
        'policy': project_form.policy,
        'potential_problems': project_form.potential_problems,
        'required_budget': project_form.required_budget,
        'project_phase': project_form.project_phase,
        'predict_profit': project_form.predict_profit,
        # 'required_technique': serializers.serialize('json', project_form.required_technique.all()),
        'techniques_list': Technique.get_technique_list(),
        'success': 'successful',
    }
    print(data)
    return JsonResponse(data)


def accept_project(request):
    print(request.POST['technique'])
    # project = Project.objects.get(id=request.GET['id'])
    # project.expert_applied.add(request.user.expertuser)
    # project.save()
    expert_user = get_object_or_404(ExpertUser, user=request.user)
    project = Project.objects.get(id=request.POST.get('id'))
    project_form = project.project_form
    if expert_user in project.expert_applied.all():
        return JsonResponse({
            'success': 'درخواست شما قبلا هم ارسال شده است'
        })
    else:
        technique_list = request.POST.getlist('technique')
        if len(technique_list) == 0:
            return JsonResponse({
                'success': 'متاسفانه بدون انتخاب تکنیک‌های موردنظر، امکان ارسال درخواست وجود ندارد.'
            })
        for technique in technique_list:
            project_technique = Technique.objects.get_or_create(technique_title=technique[:-2])
            project_form.required_technique.add(project_technique[0].id)
        project_form.save()
        project.expert_applied.add(expert_user.id)
        project.save()
        return JsonResponse({
            'success': 'درخواست شما با موفقیت ثبت شد. لطفا تا بررسی توسط صنعت مربوطه، منتظر بمانید.'
        })
    # Comment.objects.create(description="برای انجام پروژه درخواست داد. " + request.user.expertuser.expertform.__str__(
    # ) + "استاد",
    #                        expert_user=request.user.expertuser,
    #                        industry_user=project.industry_creator,
    #                        sender_type=3)
    return JsonResponse({'success': 'successful'})


def add_research_question(request):
    research_question_form = ResearchQuestionForm(request.POST, request.FILES)
    if research_question_form.is_valid():
        data = {'success': 'successful'}
        research_question = research_question_form.save(commit=False)
        research_question.expert = request.user.expertuser
        print(request.POST)
        if request.FILES.get('attachment'):
            print("tried to upload file...")
            attachment = request.FILES.get('attachment')
            research_question.attachment.save(attachment.name, attachment)
        research_question.save()
        return JsonResponse(data)
    else:
        print(research_question_form.errors)
        return JsonResponse(research_question_form.errors, status=400)


def show_research_question(request):
    research_question = ResearchQuestion.objects.filter(id=request.GET.get('id')).first()

    answers_list = []
    for answer in research_question.get_answers():
        researcher_user = ResearcherProfile.objects.get(researcher_user=answer.researcher)
        answer_json = {
            'researcher_name': researcher_user.__str__(),
            'hand_out_date': JalaliDate(answer.hand_out_date).strftime("%Y/%m/%d"),
            'is_correct': answer.is_correct,
            'answer_attachment': answer.answer.path,
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
        json_response['question_attachment_path'] = attachment.path
        json_response['question_attachment_name'] = attachment.name.split('/')[-1]
        json_response['question_attachment_type'] = attachment.name.split('/')[-1].split('.')[-1]
    return JsonResponse(json_response)


def terminate_research_question(request):
    research_question = ResearchQuestion.objects.filter(id=request.GET.get('id')).first()
    research_question.status = 'answered'
    research_question.save(update_fields=['status'])
    return JsonResponse({
        'success': 'successful'
    })


def set_answer_situation(request):
    answer = ResearchQuestionInstance.objects.filter(id=request.GET.get('id')).first()
    if request.GET.get('type') == 'true':
        answer.is_correct = 'correct'
    else:
        answer.is_correct = 'wrong'
    answer.save(update_fields=['is_correct'])
    return JsonResponse({
        'success': 'successful'
    })


def show_researcher_preview(request):
    researcher = ResearcherProfile.objects.filter(id=request.GET.get('id')).first()
    print(TechniqueInstance.objects.filter(researcher=researcher.researcher_user))
    researcher_information = {
        'photo': researcher.photo.url,
        'name': researcher.__str__(),
        'major': researcher.major,
        'grade': researcher.grade,
        'university': researcher.university,
        'entry_year': researcher.entry_year,
        'techniques': [],
        'scientific_record': serializers.serialize('json', ResearcherScientificRecord.objects.filter(researcherProfile=researcher)),
        'executive_record': serializers.serialize('json', ResearcherExecutiveRecord.objects.filter(researcherProfile=researcher)),
        'research_record': serializers.serialize('json', StudiousRecord.objects.filter(researcherProfile=researcher)),
    }
    for tech in TechniqueInstance.objects.filter(researcher=researcher.researcher_user):
        researcher_information['techniques'].append(tech.technique.technique_title)
    print(researcher_information)
    return JsonResponse(researcher_information)

def CommentForResearcher(request):
    print(request)
    form = CommentForm(request.POST ,request.FILES)
    project = Project.objects.filter(id=request.POST['project_id'])[0]
    researcher = ResearcherUser.objects.filter(id=request.POST['researcher_id'])[0]
    if form.is_valid():
        description = form.cleaned_data['description']
        attachment = form.cleaned_data['attachment']        
        comment = Comment(description=description
                         ,attachment=attachment
                         ,project=project
                         ,researcher_user=researcher
                         ,expert_user=request.user.expertuser
                         ,sender_type=0)
        comment.save()
        print(Project.objects.filter(id=request.POST['project_id']))
        data = {
            'success' : 'successful',
        }
        return JsonResponse(data)
    print("form doesn't validated!")
    return JsonResponse(form.errors ,status=400)


def CommentForIndustry(request):
    project = Project.objects.get(id=request.GET.get('id'))
    if not project.expert_messaged.objects.filter(id=request.user.expertuser.id).exists():
        project.expert_messaged.add(ExpertUser.objects.filter(id=request.user.expertuser.id))
        project.save()
    Comment.objects.create(project=project, expert_user=request.user.expertuser,
                           industry_user=project.industry_creator, description=request.GET.get('description'))

