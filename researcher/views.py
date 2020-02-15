from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, Http404 ,HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.conf import settings
from django.forms import model_to_dict
import os ,random ,datetime
from persiantools.jdatetime import JalaliDate
from dateutil.relativedelta import relativedelta
from itertools import chain
from operator import attrgetter

from . import models ,forms ,persianNumber
from expert.models import ResearchQuestion
from industry.models import Project ,Comment

def gregorian_to_numeric_jalali(date):
    j_date = JalaliDate(date)
    return str(j_date.year) + '/' + str(j_date.month) + '/' + str(j_date.day)

def date_last(date1 ,date2):
    delta = relativedelta(date1 ,date2)
    days_passed = abs(delta.days)
    months_passed = abs(delta.months)
    years_passed = abs(delta.years)
    days = ""
    months = ""
    years = ""
    if years_passed != 0:
        years = persianNumber.convert(str(years_passed)) + " سال "
    if months_passed != 0:
        if years_passed != 0:
            months = " و " + persianNumber.convert(str(months_passed)) + " ماه "
        else:
            months = persianNumber.convert(str(months_passed)) + " ماه "
    if days_passed != 0:
        if months_passed == 0 and years_passed == 0:
            days = persianNumber.convert(str(days_passed)) + " روز "
        else:
            days = " و " + persianNumber.convert(str(days_passed)) + " روز "
    if days_passed != 0 or months_passed != 0 or years_passed != 0:            
        return years + months + days
    return "امروز"


class Index(LoginRequiredMixin, generic.FormView):
    template_name = 'researcher/index.html'
    form_class = forms.InitialInfoForm
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        try:
            researcher = models.ResearcherUser.objects.get(user=request.user)
        except models.ResearcherUser.DoesNotExist:
            raise Http404('.کاربر پژوهشگر مربوطه یافت نشد')        
        if researcher.status.status == 'not_answered':
            return HttpResponseRedirect(reverse('researcher:question-alert'))
        if request.user.researcheruser.status.status == 'wait_for_answer':
            return HttpResponseRedirect(reverse('researcher:question-alert'))
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        if self.request.user.researcheruser.researchquestioninstance_set.all().count() > 0:
            context['question_instance'] = "True"
            context['uuid'] = self.request.user.researcheruser.researchquestioninstance_set.all().reverse()[0].research_question.uniqe_id
        all_projects = Project.objects.all().exclude(expert_accepted=None)
        my_projects  = all_projects.filter(researcher_applied__in=[self.request.user.researcheruser])
        new_projects = all_projects.exclude(researcher_applied__in=[self.request.user.researcheruser])
        technique_title = [str(item.technique) for item in self.request.user.researcheruser.techniqueinstance_set.all()]
        technique = models.Technique.objects.filter(technique_title__in=technique_title)
        projects = []
        for project in new_projects:
            try:
                for tech in project.project_form.required_technique.all():
                    if tech not in technique:
                        raise Exception("TECHNIQUE_NOT_EXIST")
                projects.append(project)
            except Exception:
                continue
        new_project_list = []
        for project in projects:
            if self.request.user.researcheruser in project.researcher_applied.all():
                continue
            # all_comments = project.get_comments()
            # expert_comment = all_comments.filter(sender_type=0).exclude(researcher_user=None)
            # researcher_comment = all_comments.filter(sender_type=2)
            # comments= sorted(
            #         chain(researcher_comment, expert_comment),
            #         key=attrgetter('date_submitted'))
            temp ={
                'PK'                 : project.pk,
                'project_title'      : project.project_form.project_title_persian,
                'keyword'            : project.project_form.key_words.all(),
                'started'            : date_last(datetime.date.today() ,project.date_start),
                'finished'           : date_last(datetime.date.today() ,project.date_finished),
            }
            new_project_list.append(temp)
        context['new_project_list'] = new_project_list

        done_projects = models.ResearcherHistory.objects.all()
        done_project_list = []
        for project in done_projects:
            tech_temp = [tech.technique_title for tech in project.involve_tech.all()]        
            temp = {
                'project_title' : project.title,
                'started'       : date_last(datetime.date.today(), project.start),
                'date_started'  : gregorian_to_numeric_jalali(project.start),
                # 'finished'      : date_last(datetime.date.today(), project.end),
                'date_finished' : gregorian_to_numeric_jalali(project.end),
                'delta_date'    : date_last(project.start ,project.end),
                'status'        : project.status,
                'point'         : project.point,
                'income'        : project.income,
                'technique'     : tech_temp,
            }
            done_project_list.append(temp)
        context['done_project_list'] = done_project_list

        if len(my_projects) != 0:
            evaluation_history = models.ResearcherEvaluation.objects.filter(project_title=my_projects[0].project_form.project_title_english)
            my_project_list = []
            for project in my_projects:
                title = project.project_form.project_title_english
                temp = {
                    'PK'            : project.pk,
                    'project_title' : project.project_form.project_title_persian,
                    'keyword'       : project.project_form.key_words.all(),
                    'started'       : date_last(datetime.date.today() ,project.date_start),
                    'finished'      : date_last(datetime.date.today() ,project.date_finished),
                }
                my_project_list.append(temp)
            context["my_project_list"] = my_project_list
        else:
            context["my_project_list"] = "None"
        return context

    def post(self, request, *args, **kwargs):
        researcher = get_object_or_404(models.ResearcherUser, user=request.user)
        form = forms.InitialInfoForm(request.POST, request.FILES)
        if form.is_valid():
            researcher_profile = form.save(commit=False)
            researcher_profile.researcher_user = researcher
            researcher_profile.save()
            if request.FILES.get('photo'):
                photo = request.FILES.get('photo')
                researcher_profile.photo.save(photo.name, photo)
            status = models.Status.objects.get(researcher_user=researcher)
            status.status = 'not_answered'
            status.save()
            return HttpResponseRedirect(reverse('researcher:index'))

        return super().post(self, request, *args, **kwargs)

class UserInfo(generic.TemplateView):
    template_name = 'researcher/userInfo.html'
    form_class = forms.ResearcherProfileForm


    def get(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated) or (not models.ResearcherUser.objects.filter(user=self.request.user).count()):
            return HttpResponseRedirect(reverse('chamran:login'))
        try:
            self.request.user.researcheruser.researcherprofile
        except:
            return HttpResponseRedirect(reverse("researcher:index"))    
        if request.user.researcheruser.status.status == 'not_answered':
            return HttpResponseRedirect(reverse('researcher:question-alert'))
        if request.user.researcheruser.status.status == 'wait_for_answer':
            return HttpResponseRedirect(reverse('researcher:question-alert'))
        return super().get(request, *args, **kwargs)    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.ResearcherProfileForm(self.request.user,
                                           instance=self.request.user.researcheruser.researcherprofile,
                                           initial={
                                                'grade':
                                                    self.request.user.researcheruser.researcherprofile.grade,
                                                'email':
                                                    self.request.user.username})
        # context = {
        #             'form' :  forms.ResearcherProfileForm(self.request.user,
        #                                    instance=self.request.user.researcheruser.researcherprofile,
        #                                    initial={
        #                                         'grade':
        #                                             self.request.user.researcheruser.researcherprofile.grade,
        #                                         'email':
        #                                             self.request.user.username})
        #             }
        context['scientificrecord_set'] = self.request.user.researcheruser.researcherprofile.scientificrecord_set.all()
        context['executiverecord_set'] = self.request.user.researcheruser.researcherprofile.executiverecord_set.all()
        context['studiousrecord_set'] = self.request.user.researcheruser.researcherprofile.studiousrecord_set.all()
        context['researcher_form'] = self.request.user.researcheruser.researcherprofile
        if self.request.user.researcheruser.researchquestioninstance_set.all().count() > 0:
            context['question_instance'] = "True"
            context['uuid'] = self.request.user.researcheruser.researchquestioninstance_set.all().reverse()[0].research_question.uniqe_id 
        return context

    def post(self, request, *args, **kwargs):        
        form = forms.ResearcherProfileForm(self.request.user ,request.POST, request.FILES,
                                        #    initial={
                                        #        'grade':
                                        #            self.request.user.researcheruser.researcherprofile.grade})
        )
        if form.is_valid():
            profile = request.user.researcheruser.researcherprofile
            if form.cleaned_data['photo'] is not None:
                if profile.photo:
                    if os.path.isfile(profile.photo.path):
                        os.remove(profile.photo.path)
                    profile.photo = form.cleaned_data['photo']
                else:
                    profile.photo = form.cleaned_data['photo']
            profile.address = form.cleaned_data['address']
            profile.email = form.cleaned_data['email']
            profile.home_number = form.cleaned_data['home_number']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.grade = form.cleaned_data['grade']
            if form.cleaned_data['team_work'] is not None:
                profile.team_work = form.cleaned_data['team_work']
            if form.cleaned_data['creative_thinking'] is not None:
                profile.creative_thinking = form.cleaned_data['creative_thinking']
            if form.cleaned_data['interest_in_major'] is not None:
                profile.interest_in_major = form.cleaned_data['interest_in_major']
            if form.cleaned_data['motivation'] is not None:
                profile.motivation = form.cleaned_data['motivation']
            if form.cleaned_data['sacrifice'] is not None:
                profile.sacrifice = form.cleaned_data['sacrifice']
            if form.cleaned_data['diligence'] is not None:
                profile.diligence = form.cleaned_data['diligence']
            if form.cleaned_data['interest_in_learn'] is not None:
                profile.interest_in_learn = form.cleaned_data['interest_in_learn']
            if form.cleaned_data['punctuality'] is not None:
                profile.punctuality = form.cleaned_data['punctuality']
            if form.cleaned_data['data_collection'] is not None:
                profile.data_collection = form.cleaned_data['data_collection']
            if form.cleaned_data['project_knowledge'] is not None:
                profile.project_knowledge = form.cleaned_data['project_knowledge']
            profile.description = form.cleaned_data['description']

            profile.save()
            return HttpResponseRedirect(reverse("researcher:index"))
        context=self.get_context_data(**kwargs)
        
        if form.errors['home_number']:
            context['home_number_error'] = form.errors['home_number']

        if form.errors['phone_number']:
            context['phone_number_error'] = form.errors['phone_number']

        return render(request ,'researcher/userInfo.html' ,context=context)

def ajax_ScientificRecord(request):    
    form = forms.ScientificRecordForm(request.POST)
    if form.is_valid():
        scientific_record = form.save(commit=False)
        scientific_record.researcherProfile = request.user.researcheruser.researcherprofile
        scientific_record.save()
        data = {
            'success' : 'successful',
            'pk' : scientific_record.pk,
        }
        return JsonResponse(data)
    else:
        print("error happened")
        return JsonResponse(form.errors ,status=400)

def ajax_ExecutiveRecord(request):
    form = forms.ExecutiveRecordForm(request.POST)
    if form.is_valid():
        executive_record = form.save(commit=False)
        executive_record.researcherProfile = request.user.researcheruser.researcherprofile
        executive_record.save()
        data = {
            'success' : 'successful',
            'pk' : executive_record.pk,
        }
        return JsonResponse(data)
    else:
        print("error happened")
        return JsonResponse(form.errors ,status=400)

def ajax_StudiousRecord(request):
    form = forms.StudiousRecordForm(request.POST)
    if form.is_valid():
        studious_record = form.save(commit=False)
        studious_record.researcherProfile = request.user.researcheruser.researcherprofile
        studious_record.save()
        data = {
            'success' : 'successful',
            'pk' : studious_record.pk,
        }
        return JsonResponse(data)
    else:
        return JsonResponse(form.errors ,status=400)

def signup(request, username):
    user = get_object_or_404(User, username=username)
    researcher = models.ResearcherUser(user=user)
    researcher.save()
    return HttpResponseRedirect(reverse('researcher:index'))


class Messages(generic.TemplateView):
    template_name = 'researcher/messages.html'

class Technique(generic.TemplateView):
    template_name = 'researcher/technique.html'

    def get(self, request, *args, **kwargs):
        if (not request.user.is_authenticated) or (not models.ResearcherUser.objects.filter(user=request.user).count()):
            return HttpResponseRedirect(reverse('chamran:login'))

        if request.user.researcheruser.status.status == 'not_answered':
            return HttpResponseRedirect(reverse('researcher:question-alert'))
        if request.user.researcheruser.status.status == 'wait_for_answer':
            return HttpResponseRedirect(reverse('researcher:question-alert'))

        return render(request ,self.template_name ,context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['technique_list'] = self.request.user.researcheruser.techniqueinstance_set.all()
        return context

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
        query.append(list(models.Technique.objects.filter(technique_type=tp).values_list('technique_title' ,flat=True)))
        query[-1].append(tp)
    data = {}
    for q in query:
        if len(q) > 1:
            data[q[-1]] = q[:-1]
    return JsonResponse(data=data)

def AddTechnique(request):
    form = forms.TechniqueInstanceForm(request.user ,request.POST ,request.FILES)    
    if form.is_valid():
        technique_title = form.cleaned_data['technique'] 
        method = form.cleaned_data['confirmation_method']
        resume = form.cleaned_data['resume']
        if method == 'exam':
            method_fa = "درخواست آزمون آنلاین"
        elif method == 'certificant':
            method_fa = "گواهی نامه"
        else:
            method_fa = "مقاله"
        subject = 'Technique Validation'
        message ="""کاربر به نام کاربری {} و به نام {} {} ، تکنیک {} را افزوده است.
        برای ارزیابی گزینه {} را انتخاب کرده است. لطفا {}را ارزیابی کنید و نتیجه را اعلام نمایید.
        با تشکر""".format(request.user.username ,request.user.researcheruser.researcherprofile.first_name,
                        request.user.researcheruser.researcherprofile.last_name,
                        technique_title ,method_fa ,request.user.username)
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER,],
                fail_silently=False
            )
        except TimeoutError:
            return HttpResponse('Timeout Error!!')
        try:
            technique = get_object_or_404(models.Technique ,technique_title=technique_title)
        except:
            technique_type = TECHNIQUES[technique_title]
            technique = models.Technique(technique_type=technique_type ,technique_title=technique_title)
            technique.save()
        if method == 'exam':
            technique_instance = models.TechniqueInstance(researcher=request.user.researcheruser,
                                                    technique=technique,
                                                    evaluat_date=datetime.date.today())
            technique_instance.save()
            data = {'success' : 'successful',
                    'title'   : technique_title}
            return JsonResponse(data=data)
        technique_instance = models.TechniqueInstance(researcher=request.user.researcheruser,
                                                    technique=technique,
                                                    resume=resume)
        technique_instance.save()
        data = {'success' : 'successful',
                'title'   : technique_title}
        return JsonResponse(data=data)
    return JsonResponse(form.errors ,status=400)

class Question(generic.TemplateView):
    template_name = 'researcher/question.html'

    def get(self, request, *args, **kwargs):
        if (not request.user.is_authenticated) or (not models.ResearcherUser.objects.filter(user=request.user).count()):
            return HttpResponseRedirect(reverse('chamran:login'))
        researcher = models.ResearcherUser.objects.get(user=request.user)
        if researcher.status.status == 'not_answered':
            if researcher.researchquestioninstance_set.all().count():
                question = self.request.user.researcheruser.researchquestioninstance_set.all().reverse()[0]
                return HttpResponseRedirect(reverse('researcher:question-show' ,kwargs={'question_id' : question.research_question.uniqe_id}))
            return super().get(self, request, *args, **kwargs)
        elif researcher.status.status == "wait_for_answer":
            self.template_name = "researcher/layouts/waiting_for_question.html"
            return super().get(self, request, *args, **kwargs)
        else:
            raise Http404('شما به سوال ارزیابی پاسخ داده اید.')
        return super().get(self, request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.researcheruser.researchquestioninstance_set.all().count() > 0:
            context['question_instance'] = "True"
            context['uuid'] = self.request.user.researcheruser.researchquestioninstance_set.all().reverse()[0].research_question.uniqe_id
        return context

    def post(self, request, *args, **kwargs):
        question_list = ResearchQuestion.objects.filter(status='not_answered')
        if len(question_list) == 0:
            return HttpResponseRedirect(reverse('researcher:index'))
        question = question_list[random.randint(0 ,len(question_list)-1)]
        question_instance = models.ResearchQuestionInstance(research_question=question
                                                            ,researcher = request.user.researcheruser)
        question_instance.save()
        return HttpResponseRedirect(reverse('researcher:question-show' ,kwargs={"question_id" :question.uniqe_id}))

class QuestionShow(generic.TemplateView ):
    template_name = 'researcher/layouts/preview_question.html'

    def get(self ,request ,*args, **kwargs):
        if (not request.user.is_authenticated) or (not models.ResearcherUser.objects.filter(user=request.user).count()):
            return HttpResponseRedirect(reverse('chamran:login'))
        if kwargs['question_id'] != request.user.researcheruser.researchquestioninstance_set.all().reverse()[0].research_question.uniqe_id:
            raise Http404("سوال مورد نظر پیدا نشد.")
        question = request.user.researcheruser.researchquestioninstance_set.all().reverse()[0]        
        deltatime = datetime.date.today() - question.hand_out_date
        if deltatime.days < 8:
            if question.is_answered:
                print("+_+_+_+_+_+_+_+_+_+_====")
                return HttpResponseRedirect(reverse('researcher:index'))
            if question.is_correct == "correct" :
                request.user.researcheruser.status.status = 'free'
                request.user.researcheruser.status.status.save()
        else:
            status = request.user.researcheruser.status
            status.status = 'inactivated'
            inactivate_date = datetime.date.today()+ datetime.timedelta(days=30)
            status.inactivate_duration = inactivate_date
            status.save()
        return super().get(request ,args, kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = models.ResearchQuestionInstance.objects.filter(researcher=self.request.user.researcheruser).reverse()[0]
        deltatime = datetime.date.today() - question.hand_out_date
        context['question_title'] = question.research_question.question_title
        context['question'] = question.research_question.question_text
        context['attachment'] = question.research_question.attachment
        context['attach_type'] = str(question.research_question.attachment).split("/")[-1].split('.')[-1]
        context['file_name'] = question.research_question.attachment.name.split("/")[-1]
        delta = datetime.date.today() - question.hand_out_date
        context['day']  = 8 - delta.days
        context['hour'] = 23 - datetime.datetime.now().hour
        context['minute'] = 59 - datetime.datetime.now().minute
        return context
    
    def post(self ,request ,*args, **kwargs):
        question = self.request.user.researcheruser.researchquestioninstance_set.all().reverse()[0]
        uuid_id = question.research_question.uniqe_id
        if 'answer' in request.FILES:
            question.answer = request.FILES['answer']
            question.is_answered = True
            question.save()
            request.user.researcheruser.status.status = 'free'
            request.user.researcheruser.status.save()
            subject = 'Research Question Validation'
            message ="""با عرض سلام و خسته نباشید.
            پژوهشگر {} به نام {} {} به سوال پژوهشی {} پاسخ داده است.
            لطفا پاسخ پژوهشگر را ارزیابی نمایید.
            با تشکر""".format(self.request.user.username ,self.request.user.researcheruser.researcherprofile.first_name,
                            self.request.user.researcheruser.researcherprofile.last_name,
                            question.research_question.question_title)
            email = question.research_question.expert.user.username
            try:
                send_mail(  
                    subject=subject,
                    message=message, 
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                )
            except TimeoutError:
                return HttpResponse('Timeout Error!!')
        return HttpResponseRedirect(reverse("researcher:question-show" ,kwargs={"question_id" :uuid_id}))
    
def ajax_Technique_review(request):
    form = forms.TechniqueReviewFrom(request.POST ,request.FILES)
    if form.is_valid():
        description = form.cleaned_data['request_body']
        method = form.cleaned_data['request_confirmation_method']
        technique = request.user.researcheruser.techniqueinstance_set.all().filter(technique__technique_title=request.POST['technique_name'])[0]
        if method != "exam":
            resume = form.cleaned_data['new_resume']
            technique_review = models.TechniqueReview(technique_instance = technique,description=description,
                                                      method=method ,resume=resume)
        else:
            technique_review = models.TechniqueReview(technique_instance = technique,description=description,
                                                      method=method)
        technique_review.save()
        subject = 'Research Question Validation'
        message ="""با عرض سلام و خسته نباشید.
        پژوهشگر {} در خواست ارتفا سطح تکنیک {} را از طریق {} داده است.
        لطفا درخواست وی را ارزیابی نمایید.
        با تشکر""".format(request.user.username ,request.user.researcheruser.researcherprofile.first_name,
                        request.user.researcheruser.researcherprofile.last_name)
        try:
            send_mail(
                subject=subject,
                message=message, 
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
            )
        except TimeoutError:
            return HttpResponse('Timeout Error!!')
        data = {'success' : 'successful'}
        return JsonResponse(data)
    return JsonResponse(form.errors ,status=400)

def ShowProject(request):
    project = Project.objects.filter(id=request.GET.get('id')).first()
    json_response = model_to_dict(project.project_form)
    json_response['deadline'] = 'نا مشخص'
    if project.status == 1 and project.date_project_started and project.date_phase_three_deadline:
        json_response['deadline'] = date_last(datetime.date.today() ,project.date_phase_three_deadline)
    else:
        json_response['deadline'] = date_last(project.date_project_started, project.date_phase_three_deadline)
    json_response['submission_date'] = gregorian_to_numeric_jalali(project.date_submitted_by_industry)
    for ind, value in enumerate(json_response['key_words']):
        json_response['key_words'][ind] = value.__str__()
    json_response['required_technique']=[]
    for tech in project.project_form.required_technique:
        json_response['required_technique'].append(tech.__str__())
    all_comments = project.get_comments().exclude(researcher_user=None)
    json_response['comments'] = []
    for com in all_comments:
        try:
            url = com.attachment.url[com.attachment.url.find('media' ,2):]
        except:
            url = "None"
        temp = {
            'pk'           : com.pk,
            'description'  : com.description,
            'replied_text' : com.replied_text,
            'sender_type'  : com.sender_type,
            'attachment'   : url
        }
        json_response['comments'].append(temp)
        if com.sender_type == expert:
            com.status = 'seen'
            com.save()
    return JsonResponse(json_response)

def DeleteComment(request):
    try:
        comment = get_object_or_404(Comment ,pk=request.POST['id'])
        comment.delete()
    except:
        return JsonResponse({} ,400)
    return JsonResponse({'successful' :"successful"})

def ApplyProject(request):
    form = forms.ApplyForm(request.POST)
    if form.is_valid():
        project=get_object_or_404(Project ,id=request.POST['id'])
        least_hour = form.cleaned_data['least_hours']
        most_hour = form.cleaned_data['most_hours']
        apply_project = models.RequestedProject(researcher=request.user.researcheruser,
                                                project=project,
                                                least_hours_offered=least_hour,
                                                most_hours_offered=most_hour)
        apply_project.save()
        comment = Comment(description="درخواست شما برای استاد پروژه فرستاده شد.",
                          sender_type="system",
                          project=project,
                          researcher_user=request.user.researcheruser,
                          status='unseen')
        comment.save()
        project.researcher_applied.add(request.user.researcheruser)
        return JsonResponse(data={'success' : "success"})
    return JsonResponse(form.errors ,status=400)

def MyProject(request):    
    project = Project.objects.filter(id=request.GET.get('id')).first()
    json_response = model_to_dict(project.project_form)
    json_response['deadline'] = 'نا مشخص'
    if project.status == 1 and project.date_project_started and project.date_phase_three_deadline:
        json_response['deadline'] = date_last(datetime.date.today() ,project.date_phase_three_deadline)
    else:
        json_response['deadline'] = date_last(project.date_project_started, project.date_phase_three_deadline)
    json_response['submission_date'] = gregorian_to_numeric_jalali(project.date_submitted_by_industry)
    for ind, value in enumerate(json_response['key_words']):
        json_response['key_words'][ind] = value.__str__()
    json_response['required_technique']=[]
    for tech in project.project_form.required_technique:
        json_response['required_technique'].append(tech.__str__())
    all_comments = project.get_comments().exclude(researcher_user=None)
    json_response['comments'] = []
    for com in all_comments:
        try:
            url = com.attachment.url[com.attachment.url.find('media' ,2):]
        except:
            url = "None"
        temp = {
            'pk'           : com.pk,
            'description'  : com.description,
            'replied_text' : com.replied_text,
            'sender_type'  : com.sender_type,
            'attachment'   : url
        }
        json_response['comments'].append(temp)
    title = project.project_form.project_title_english
    evaluation_history = models.ResearcherEvaluation.objects.filter(project_title=title)
    json_response['vote'] = "false"
    if datetime.date.today() > project.date_finished:
        if len(evaluation_history.filter(phase=3)) == 0:
            json_response['vote'] = "true"
    elif datetime.date.today() > project.date_phase_two_finished:
        if len(evaluation_history.filter(phase=2)) == 0:
            json_response['vote'] = "true"
    elif datetime.date.today() > project.date_phase_one_finished:
        if len(evaluation_history.filter(phase=1)) == 0:
            json_response['vote'] = "true"
    return JsonResponse(json_response)
#     else:
#         return JsonResponse(data={'error' :'پروژه فعالی برای شما ثبت نشده است.'})

# def DoneProjects(request):
#     projects = models.ResearcherHistory.objects.all()
#     project_list = {}    
#     for project in projects:
#         tech_temp = [tech.technique_title for tech in project.involve_tech.all()]        
#         project_list[project.title] = {
#             'project_title' : project.title,
#             'started'       : date_last(datetime.date.today(), project.start),
#             'finished'      : date_last(datetime.date.today(), project.end),
#             'status'        : project.status,
#             'point'         : project.point,
#             'income'        : project.income,
#             'technique'     : tech_temp,
#         }
#     return JsonResponse(data={"project_list" : project_list})

def AddComment(request):
    form = forms.CommentForm(request.POST ,request.FILES)
    project = Project.objects.filter(id=request.POST['project_id'])[0]
    if form.is_valid():
        description = form.cleaned_data['description']
        attachment = form.cleaned_data['attachment']        
        comment = Comment(description=description
                         ,attachment=attachment
                         ,project=project
                         ,researcher_user=request.user.researcheruser
                         ,expert_user=project.expert_accepted
                         ,sender_type="researcher"
                         ,status='unseen')
        comment.save()
        if attachment is not None:
            data = {
                'success' : 'successful',
                'attachment' : comment.attachment.url[comment.attachment.url.find('media' ,2):],
                'description':description,
                'pk' : comment.pk,
            }
        else:
            data = {
                'success' : 'successful',
                'attachment' : "None",
                'description': description,
                'pk' : comment.pk,
            }
        return JsonResponse(data)
    return JsonResponse(form.errors ,status=400)

def DeleteScientificRecord(request):
    try:
        sci_rec = get_object_or_404(models.ScientificRecord ,pk=request.POST['pk'])
    except:
        return JsonResponse({"errors" :"Scientific record isn't found"} ,status=400)
    sci_rec.delete()
    return JsonResponse({"successfull" :"Scientific record is deleted"})

def DeleteExecutiveRecord(request):
    try:
        exe_rec = get_object_or_404(models.ExecutiveRecord ,pk=request.POST['pk'])
    except:
        return JsonResponse({"errors" :"Executive record isn't found"} ,status=400)
    exe_rec.delete()
    return JsonResponse({"successfull" :"Executive record is deleted"})

def DeleteStudiousRecord(request):
    try:
        stu_rec = get_object_or_404(models.StudiousRecord ,pk=request.POST['pk'])
    except:
        return JsonResponse({"errors" :"Studious record isn't found"} ,status=400)
    stu_rec.delete()
    return JsonResponse({"successfull" :"Studious record is deleted"})

TECHNIQUES = {
    'Polymerase Chain Reaction' :'Molecular Biology',
    'RNA-Seq' :'Molecular Biology',
    'DNA Metylation Analysis' :'Molecular Biology',
    'DNA Gel Electorphoresis' :'Molecular Biology',
    'Two-Dimensional Gel Electorphoresis' :'Molecular Biology',
    'Gel Purification' :'Molecular Biology',
    'DNA Ligation Reaction' :'Molecular Biology',
    'Restriction Enzyme Digests' :'Molecular Biology',
    'Bacterial Culture' :'Molecular Biology',
    'Bacterial Transformation The Heat Shock Method' :'Molecular Biology',
    'Bacterial Transformation Electroporation' :'Molecular Biology',
    'Plasmid Purification' :'Molecular Biology',
    'The Western Bolt' :'Molecular Biology',
    'The Northern Bolt' :'Molecular Biology',
    'Co-Immunoprecipition and Pull-Down Assays' :'Molecular Biology',
    'Expression Profiling with Microarrays' :'Molecular Biology',
    'Cytogenetics' :'Molecular Biology',
    'Chromatin Immunoprecipition' :'Molecular Biology',
    'Recombineering and Gene Targeting' :'Molecular Biology',
    'SNP Genotyping' :'Molecular Biology',
    'Genome Editing' :'Molecular Biology',
    'Gene Silencing' :'Molecular Biology',

    'The ELISA Method' :'Immunology',
    'Flow Cytometry' :'Immunology',
    'Flow cell storing' :'Immunology',
    'Magnetice Bead cell Isolation' :'Immunology',

    'SEM Imaging of Biological Samples' :'Imaging',
    'Biodistribution of Nano-drog Carriers Applications of SEM' :'Imaging',
    'Imaging of Biological Samples with Optical and Confocal Microscopy' :'Imaging',
    'Calcium Imaging in Neurons' :'Imaging',
    'Animal Flourescene' :'Imaging',
    'Animal CT' :'Imaging',
    'Animal MRI' :'Imaging',
    'Animal SPECT' :'Imaging',
    'Animal PET' :'Imaging',
    'Animal US' :'Imaging',

    'Sterile Tissue Harvest' :'Histology',
    'Diagnostic Necropsy and Tissue Harvest' :'Histology',
    'Tissue Cryopreservation' :'Histology',
    'Tissue Fixation' :'Histology',
    'Microtome Sectioning' :'Histology',
    'Cryostat Sectioning' :'Histology',
    'H&E staining' :'Histology',
    'Histochemistry' :'Histology',
    'Histoflouresence' :'Histology',

    'An Introduction to the Centrifuge' :'General Lab',
    'Regulating Temperature in the Lab Preserving Samples Using Cold' :'General Lab',
    'Introduction to the Bunsen Burner' :'General Lab',
    'Introduction to Serological Pipettes and Pipettor' :'General Lab',
    'An Introduction to the Micropipettor' :'General Lab',
    'Making Solutions in the Laboratory' :'General Lab',    
    'Understanding Concentration and Measuring Volumes' :'General Lab',
    'Introduction to the Microplate Reader' :'General Lab',
    'Regulation Temperature in the Lab Applying Heat' :'General Lab',
    'Common Lab Glassware and Users' :'General Lab',
    'Solutions and Concentrations' :'General Lab',
    'Determining the Density of a Solid and Liquid' :'General Lab',
    'Determining the Mass Percent Composition in an Aqueous Solution' :'General Lab',
    'Determining the Empirical Formula' :'General Lab',
    'Determining the Solubility Rules of Ionic Compounds' :'General Lab',
    'Using a pH Meter' :'General Lab',
    'Introduction to Titration' :'General Lab',
    'Ideal Gas Law' :'General Lab',

    'An Introduction to Working in Hood' :'Lab Safety',
    'Operation of High-pressure Reactor Vessels' :'Lab Safety',
    'Decontamination for laboratory Biosafety Proper Waste Disposal' :'Lab Safety',
    'Fume Hoods and Laminar Flow Cabinates' :'Lab Safety',
    'Handling Chemical Spills' :'Lab Safety',
    'Chemical Storage Categories,Hazards and Compatibilies' :'Lab Safety',
    'Guidelines in Case of an Laboratory Emergency' :'Lab Safety',
    'Work with Hot and Cold Sources' :'Lab Safety',
    'Electrical Safety' :'Lab Safety',
    'Emergency Eyewash and Shower Stations' :'Lab Safety',
    'Proper Personal Protective Equipment' :'Lab Safety',

    'Serearching on articles resources' :'Research Methodology',
    'Endnote' :'Research Methodology',
    'spss/graph pad' :'Research Methodology',
    'Essy writing' :'Research Methodology',
    'Poster Presentation' :'Research Methodology',
    'Microsoft Office' :'Research Methodology',
    'Photoshop' :'Research Methodology',

    'Introduction to the Spectrophotometer' :'Biochemistry',
    'Measuring Mass in the Laboratory' :'Biochemistry',
    'NMR' :'Biochemistry',
    'X-ray Fluorescence(XRF)' :'Biochemistry',
    'Gas Chromatography(GC) with Flame-lonization Detection' :'Biochemistry',
    'High-Performance Liquid Chromatography(HPLC)' :'Biochemistry',
    'Ion-Exchange Chromatography' :'Biochemistry',
    'Chromatography-based Biomolecule Purification Methods' :'Biochemistry',
    'Capillary Electrophoresis(CE)' :'Biochemistry',
    'Introduce to Mass Spectrometry' :'Biochemistry',
    'Scanning Electron Microscopy(SEM)' :'Biochemistry',
    'Cyclic Voltammetry(CV)' :'Biochemistry',
    'MALDI-TOF Mass Spectrometry' :'Biochemistry',
    'Tandem Mass Spectrometry' :'Biochemistry',
    'Protein Crystallization' :'Biochemistry',
    'Electrophoretic Mobility Shift Assay(EMSA)' :'Biochemistry',
    'Photometric Protein Determination' :'Biochemistry',
    'Density Gradient Ultracentrifugation' :'Biochemistry',
    'Forster Resonance Energy Transfer(FRET)' :'Biochemistry',
    'Surface Plasmon Resonance(SPR)' :'Biochemistry',
    'Synthetic Organic Chemestry' :'Biochemistry',

    'An Introduction to the Laboratory Mouse Mos Musculus' :'Animal Lab',
    'Rodent Handling and Restraint Techniques' :'Animal Lab',
    'Basic Mouse Care and Maintenance' :'Animal Lab',
    'Development and Reproduction of the Laboratory Mouse' :'Animal Lab',
    'Basic Care Procedures' :'Animal Lab',
    'Fundamentals of Breeding and Weaning' :'Animal Lab',
    'Rodent Identification I' :'Animal Lab',
    'Rodent Identification II' :'Animal Lab',
    'Compound Administration I' :'Animal Lab',
    'Compound Administration II' :'Animal Lab',
    'Compound Administration III' :'Animal Lab',
    'Compound Administration IV' :'Animal Lab',
    'Blood Withdrawal I' :'Animal Lab',
    'Anesthesia Introduction and Maintenance' :'Animal Lab',
    'Rodent Stereoxtic Surgery' :'Animal Lab',
    'Considerations for Rodent Surgery' :'Animal Lab',

    'Whole-Mount in Situ Hybridization' :'Cellular Biology',
    'Molecular Cloning' :'Cellular Biology',
    'Yeast Transformation and Cloning' :'Cellular Biology',
    'Embryonic Steam Cell Culture and Differentiaton' :'Cellular Biology',
    'An Introduction to Transfection' :'Cellular Biology',
    'Transduction' :'Cellular Biology',
    'Introduction to Light Microscopy' :'Cellular Biology',
    'Introduction to Fluorescence Microscopy' :'Cellular Biology',
    'Histological Sample Preparation for Light Microscopy' :'Cellular Biology',
    'Cell-surface Biotinylation Assay' :'Cellular Biology',
}

# 7072488c-02ab-4362-9e51-7100dae78473
#persiontools