from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, Http404, HttpResponse
from django.views import generic
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.conf import settings
from django.forms import model_to_dict
import os, random, datetime
from persiantools.jdatetime import JalaliDate
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import permission_required

from django.utils import timezone

from . import models, forms, persianNumber
from expert.models import ResearchQuestion, RequestResearcher
from industry.models import Project, Comment
from chamran_admin.models import Message

ACCELERATOR = "384025"


def get_url(rawUrl):
    return rawUrl[rawUrl.find('media', 2):]


def gregorian_to_numeric_jalali(date):
    j_date = JalaliDate(date)
    return str(j_date.year) + '/' + str(j_date.month) + '/' + str(j_date.day)


def date_last(date1, date2):
    delta = relativedelta(date1, date2)
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


class Index(LoginRequiredMixin, PermissionRequiredMixin, generic.FormView):
    template_name = 'researcher/index.html'
    form_class = forms.InitialInfoForm
    success_url = "/researcher/"
    login_url = '/login/'
    permission_required = ('researcher.be_researcher',)

    def get(self, request, *args, **kwargs):
        researcher = models.ResearcherUser.objects.get(user=request.user)
        status = researcher.status
        if status.status == 'deactivated':
            if status.is_deactivated:
                status.status = 'not_answered'
                status.save()
        STATUS = ['wait_for_result', 'not_answered']
        if status.status in STATUS:
            return HttpResponseRedirect(reverse('researcher:question-alert'))
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        researcher = self.request.user.researcheruser
        context['status'] = researcher.status.status
        if researcher.status.status == 'deactivated':
            return context
        all_projects = [re.project.pk for re in RequestResearcher.objects.filter(researcher_count__gte=0)]
        all_projects = Project.objects.filter(id__in=all_projects)
        my_projects = all_projects.filter(researcher_applied__in=[researcher])
        new_projects = all_projects.exclude(researcher_applied__in=[researcher])
        technique_title = [str(item.technique) for item in researcher.techniqueinstance_set.all()]
        technique = models.Technique.objects.filter(technique_title__in=technique_title)
        projects = []
        missedProjects = []
        missedTechnique = []
        for project in new_projects:
            missedTechnique = []
            for tech in project.project_form.required_technique.all():
                if tech not in technique:
                    missedTechnique.append(tech.technique_title)
            if len(missedTechnique):
                missedProjects.append({'project': project, "missedTechnique": missedTechnique})
            else:
                projects.append(project)
        new_project_list = []
        missed_project_list = []
        for project in projects:
            if researcher in project.researcher_applied.all():
                continue
            temp = {
                'PK': project.pk,
                'project_title': project.project_form.project_title_persian,
                'keyword': project.project_form.key_words.all(),
                'started': date_last(datetime.date.today(), project.date_start),
                'finished': date_last(datetime.date.today(), project.date_finished),
                'need_hour': project.requestresearcher.least_hour,
            }
            new_project_list.append(temp)
        for project in missedProjects:
            temp = {
                'project_title': project["project"].project_form.project_title_persian,
                'keyword': project["project"].project_form.key_words.all(),
                'started': date_last(datetime.date.today(), project["project"].date_start),
                'finished': date_last(datetime.date.today(), project["project"].date_finished),
                'need_hour': project["project"].requestresearcher.least_hour,
                'missedTechinque': project["missedTechnique"],
            }
            missed_project_list.append(temp)
        context['new_project_list'] = new_project_list
        context['missed_project_list'] = missed_project_list

        done_projects = models.ResearcherHistory.objects.all()
        done_project_list = []
        for project in done_projects:
            tech_temp = [tech.technique_title for tech in project.involve_tech.all()]
            temp = {
                'project_title': project.title,
                'started': date_last(datetime.date.today(), project.start),
                'date_started': gregorian_to_numeric_jalali(project.start),
                # 'finished'      : date_last(datetime.date.today(), project.end),
                'date_finished': gregorian_to_numeric_jalali(project.end),
                'delta_date': date_last(project.start, project.end),
                'status': project.status,
                'point': project.point,
                'income': project.income,
                'technique': tech_temp,
            }
            done_project_list.append(temp)
        context['done_project_list'] = done_project_list

        my_project_list = []
        if len(my_projects) != 0:
            evaluation_history = models.ResearcherEvaluation.objects.filter(
                project_title=my_projects[0].project_form.project_title_english)
            for project in my_projects:
                title = project.project_form.project_title_english
                status = "در حال بررسی"
                if researcher in project.researcher_accepted.all():
                    status = "قبول"
                if researcher in project.researcher_banned.all():
                    status = "رد شده"
                temp = {
                    'PK': project.pk,
                    'project_title': project.project_form.project_title_persian,
                    'keyword': project.project_form.key_words.all(),
                    'started': date_last(datetime.date.today(), project.date_start),
                    'finished': date_last(datetime.date.today(), project.date_finished),
                    'need_hour': project.requestresearcher.least_hour,
                    'status': status,
                }
                my_project_list.append(temp)
        context["my_project_list"] = my_project_list
        return context

    def form_valid(self, form):
        researcher = get_object_or_404(models.ResearcherUser, user=self.request.user)
        researcher_profile = form.save(commit=False)
        researcher_profile.researcher_user = researcher
        researcher_profile.save()
        if "photo" in self.request.FILES.keys():
            if self.request.FILES.get('photo'):
                photo = self.request.FILES.get('photo')
                researcher_profile.photo.save(photo.name, photo)
        status = models.Status.objects.get(researcher_user=researcher)
        status.status = 'not_answered'
        status.save()
        return super().form_valid(form)


class UserInfo(PermissionRequiredMixin, LoginRequiredMixin, generic.TemplateView):
    template_name = 'researcher/userInfo.html'
    form_class = forms.ResearcherProfileForm
    login_url = '/login/'
    permission_required = ('researcher.be_researcher',)

    def get(self, request, *args, **kwargs):
        try:
            self.researcherProfile = self.request.user.researcheruser.researcherprofile
        except:
            return HttpResponseRedirect(reverse("researcher:index"))
        if request.user.researcheruser.status.status == 'not_answered':
            return HttpResponseRedirect(reverse('researcher:question-alert'))
        if request.user.researcheruser.status.status == 'wait_for_result':
            return HttpResponseRedirect(reverse('researcher:question-alert'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.user.researcheruser.status.status
        context["form"] = forms.ResearcherProfileForm(instance=self.researcherProfile,
                                                      initial={
                                                          'grade':
                                                              self.researcherProfile.grade,
                                                          'email':
                                                              self.request.user.username})
        context['scientificrecord_set'] = self.researcherProfile.scientificrecord_set.all()
        context['executiverecord_set'] = self.researcherProfile.executiverecord_set.all()
        context['studiousrecord_set'] = self.researcherProfile.studiousrecord_set.all()
        context['researcher_form'] = self.researcherProfile
        return context

    def post(self, request, *args, **kwargs):
        form = forms.ResearcherProfileForm(request.POST, request.FILES,
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
            if form.cleaned_data['resume'] is not None:
                profile.resume = form.cleaned_data['resume']
            # if form.cleaned_data['team_work'] is not None:
            #     profile.team_work = form.cleaned_data['team_work']
            # if form.cleaned_data['creative_thinking'] is not None:
            #     profile.creative_thinking = form.cleaned_data['creative_thinking']
            # if form.cleaned_data['interest_in_major'] is not None:
            #     profile.interest_in_major = form.cleaned_data['interest_in_major']
            # if form.cleaned_data['motivation'] is not None:
            #     profile.motivation = form.cleaned_data['motivation']
            # if form.cleaned_data['sacrifice'] is not None:
            #     profile.sacrifice = form.cleaned_data['sacrifice']
            # if form.cleaned_data['diligence'] is not None:
            #     profile.diligence = form.cleaned_data['diligence']
            # if form.cleaned_data['interest_in_learn'] is not None:
            #     profile.interest_in_learn = form.cleaned_data['interest_in_learn']
            # if form.cleaned_data['punctuality'] is not None:
            #     profile.punctuality = form.cleaned_data['punctuality']
            # if form.cleaned_data['data_collection'] is not None:
            #     profile.data_collection = form.cleaned_data['data_collection']
            # if form.cleaned_data['project_knowledge'] is not None:
            #     profile.project_knowledge = form.cleaned_data['project_knowledge']
            profile.description = form.cleaned_data['description']

            profile.save()
            return HttpResponseRedirect(reverse("researcher:index"))
        context = self.get_context_data(**kwargs)

        if form.errors['home_number']:
            context['home_number_error'] = form.errors['home_number']

        if form.errors['phone_number']:
            context['phone_number_error'] = form.errors['phone_number']

        return render(request, 'researcher/userInfo.html', context=context)


@permission_required('researcher.be_researcher', login_url='/login/')
def ajax_ScientificRecord(request):
    form = forms.ScientificRecordForm(request.POST)
    if form.is_valid():
        scientific_record = form.save(commit=False)
        scientific_record.researcherProfile = request.user.researcheruser.researcherprofile
        scientific_record.save()
        data = {
            'success': 'successful',
            'pk': scientific_record.pk,
        }
        return JsonResponse(data)
    else:
        print("error happened")
        return JsonResponse(form.errors, status=400)


@permission_required('researcher.be_researcher', login_url='/login/')
def ajax_ExecutiveRecord(request):
    form = forms.ExecutiveRecordForm(request.POST)
    if form.is_valid():
        executive_record = form.save(commit=False)
        executive_record.researcherProfile = request.user.researcheruser.researcherprofile
        executive_record.save()
        data = {
            'success': 'successful',
            'pk': executive_record.pk,
        }
        return JsonResponse(data)
    else:
        print("error happened in Executive Form")
        return JsonResponse(form.errors, status=400)


@permission_required('researcher.be_researcher', login_url='/login/')
def ajax_StudiousRecord(request):
    form = forms.StudiousRecordForm(request.POST)
    if form.is_valid():
        studious_record = form.save(commit=False)
        studious_record.researcherProfile = request.user.researcheruser.researcherprofile
        studious_record.save()
        data = {
            'success': 'successful',
            'pk': studious_record.pk,
        }
        return JsonResponse(data)
    else:
        return JsonResponse(form.errors, status=400)


class Technique(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'researcher/technique.html'
    login_url = '/login/'
    permission_required = ('researcher.be_researcher', 'researcher.is_active')

    def get(self, request, *args, **kwargs):
        if request.user.researcheruser.status.status == 'not_answered':
            return HttpResponseRedirect(reverse('researcher:question-alert'))
        if request.user.researcheruser.status.status == 'wait_for_result':
            return HttpResponseRedirect(reverse('researcher:question-alert'))

        return render(request, self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.user.researcheruser.status.status
        context['technique_list'] = self.request.user.researcheruser.techniqueinstance_set.all()
        return context


@permission_required(('researcher.be_researcher', 'researcher.is_active'), login_url='/login/')
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
        query.append(list(models.Technique.objects.filter(technique_type=tp).values_list('technique_title', flat=True)))
        query[-1].append(tp)
    data = {}
    for q in query:
        if len(q) > 1:
            data[q[-1]] = q[:-1]
    return JsonResponse(data=data)


@permission_required(('researcher.be_researcher', 'researcher.is_active'), login_url='/login/')
def AddTechnique(request):
    form = forms.TechniqueInstanceForm(request.user, request.POST, request.FILES)
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
        message = """کاربر به نام کاربری {} و به نام {} ، تکنیک {} را افزوده است.
        برای ارزیابی گزینه {} را انتخاب کرده است. لطفا {}را ارزیابی کنید و نتیجه را اعلام نمایید.
        با تشکر""".format(request.user.username, request.user.researcheruser.researcherprofile.fullname,
                          technique_title, method_fa, request.user.username)
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER, ],
                fail_silently=False
            )
        except TimeoutError:
            return HttpResponse('Timeout Error!!')
        try:
            technique = get_object_or_404(models.Technique, technique_title=technique_title)
        except:
            technique_type = TECHNIQUES[technique_title]
            technique = models.Technique(technique_type=technique_type, technique_title=technique_title)
            technique.save()
        if method == 'exam':
            technique_instance = models.TechniqueInstance(researcher=request.user.researcheruser,
                                                          technique=technique,
                                                          evaluat_date=datetime.date.today())
        else:
            technique_instance = models.TechniqueInstance(researcher=request.user.researcheruser,
                                                          technique=technique,
                                                          resume=resume)
        technique_instance.save()
        data = {'success': 'successful',
                'title': technique_title,
                "is_exam": method == 'exam',
                'link': technique.tutorial_link}
        return JsonResponse(data=data)
    return JsonResponse(form.errors, status=400)


class Question(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'researcher/question.html'
    login_url = '/login/'
    permission_required = ('researcher.be_researcher', 'researcher.is_active')

    def get(self, request, *args, **kwargs):
        self.request = request
        if (not request.user.is_authenticated) or (not models.ResearcherUser.objects.filter(user=request.user).count()):
            return HttpResponseRedirect(reverse('chamran:login'))
        researcher = models.ResearcherUser.objects.get(user=request.user)
        if researcher.status.status == 'not_answered':
            if researcher.researchquestioninstance_set.all().count():
                question = request.user.researcheruser.researchquestioninstance_set.all().reverse().first()
                return HttpResponseRedirect(
                    reverse('researcher:question-show', kwargs={'question_id': question.research_question.uniqe_id}))
            return super().get(self, request, *args, **kwargs)
        elif researcher.status.status == "wait_for_result":
            self.template_name = "researcher/layouts/waiting_for_question.html"
            return super().get(self, request, *args, **kwargs)
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.user.researcheruser.status.status
        if self.request.user.researcheruser.status.status == "wait_for_result":
            question = models.ResearchQuestionInstance.objects.filter(
                researcher=self.request.user.researcheruser).reverse().first()
            answer = question.answer
            context['answerName'] = answer.name.split(".com-")[-1]
            context["answerType"] = answer.name.split(".")[-1]
            if context["answerType"] == "jpeg":
                context["answerType"] = "jpg"
            context['answerUrl'] = answer.url
            return context
        STATUS = ["free", 'waiting', 'involved']
        if self.request.user.researcheruser.status.status in STATUS:
            context['answered'] = True
        return context

    def post(self, request, *args, **kwargs):
        question_list = ResearchQuestion.objects.filter(status='not_answered')
        researcherStatus = request.user.researcheruser.status
        if 'accelerator' in request.POST.keys() and researcherStatus.status != 'deactivated':
            if request.POST['accelerator'] == ACCELERATOR:
                title = "تایید سوال پژوهشی"
                text =  """با سلام،
پژوهشگر گرامی، پاسخ سوال پژوهشی شما پذیرفته شد.
به این ترتیب، پیوستن شما به مجموعه پژوهشگران «چمران‌تیم» را تبریک می‌گوییم و امیدواریم شاهد پیشرفت شما در زمینه پژوهش باشیم.
از این پس می‌توانید از طریق قسمت «پروژه‌ها» برای شرکت در پروژه‌های تعریف‌شده توسط مجموعه‌های پژوهشی، درخواست ارسال کنید. 
البته در نظر داشته باشید که برای شرکت در هر پروژه‌ای، لازم است مهارت‌های پژوهشی آن پروژه را قبلا کسب کرده باشید. به همین خاطر، توصیه می‌کنیم به قسمت «مهارت‌های پژوهشی» حساب کاربری‌تان هم سر بزنید و با افزایش تعداد مهارت‌های‌تان، شانس خود را برای شرکت در پروژه‌ها افزایش دهید.
همچنین، با تکمیل یا بارگذاری رزومه علمی‌تان از طریق قسمت «اطلاعات کاربری»، می‌توانید توانمندی‌های خود را در هنگام انتخاب شدن‌تان توسط استاد و یا مجموعه پژوهشی، نشان دهید.
با آرزوی موفقیت، 
چمران‌تیم"""
                messageType = 0
                try:
                    message = Message.objects.filter(title=title).first()
                except:
                    message = None
                if message is None:
                    message = Message(title=title,
                                      text=text,
                                      type=messageType)
                    message.save()
                message.receiver.add(request.user)
                message.save()
                researcherStatus.status = 'free'
                researcherStatus.save()
                return HttpResponseRedirect(reverse('researcher:index'))
        if len(question_list) == 0:
            return HttpResponseRedirect(reverse('researcher:index'))
        question = question_list[random.randint(0, len(question_list) - 1)]
        question_instance = models.ResearchQuestionInstance(research_question=question
                                                            , researcher=request.user.researcheruser)
        question_instance.save()
        return HttpResponseRedirect(reverse('researcher:question-show', kwargs={"question_id": question.uniqe_id}))


class QuestionShow(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    template_name = 'researcher/layouts/preview_question.html'
    login_url = '/login/'
    permission_required = ('researcher.be_researcher', 'researcher.is_active')

    def get(self, request, *args, **kwargs):
        if kwargs[
            'question_id'] != request.user.researcheruser.researchquestioninstance_set.all().reverse().first().research_question.uniqe_id:
            raise Http404("سوال مورد نظر پیدا نشد.")
        if self.request.user.researcheruser.status.status != "not_answered":
            return HttpResponseRedirect(reverse("researcher:question-alert"))
        question = request.user.researcheruser.researchquestioninstance_set.all().reverse().first()
        deadLine = question.hand_out_date + datetime.timedelta(days=+7)
        now = datetime.datetime.now(datetime.timezone.utc)
        if now < deadLine:
            if question.is_correct == "correct":
                request.user.researcheruser.status.status = 'free'
                request.user.researcheruser.status.save()
                self.template_name = "researcher/layouts/answered_question.html"
                return super().get(request, args, kwargs)
        elif request.user.researcheruser.status.status == "not_answered":
            status = request.user.researcheruser.status
            status.status = 'deactivated'
            inactivate_date = datetime.date.today() + datetime.timedelta(days=30)
            status.inactivate_duration_temp = inactivate_date
            status.save()
            ctype = ContentType.objects.get_for_model(models.ResearcherUser)
            permission = Permission.objects.get(content_type=ctype, codename='is_active')
            request.user.user_permissions.remove(permission)
            request.user.save()
            return HttpResponseRedirect(reverse("researcher:index"))
        return super().get(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.user.researcheruser.status.status
        question = models.ResearchQuestionInstance.objects.filter(
            researcher=self.request.user.researcheruser).reverse().first()
        context['question_title'] = question.research_question.question_title
        context['question'] = question.research_question.question_text
        context['attachment'] = question.research_question.attachment
        context['attach_type'] = str(question.research_question.attachment).split("/")[-1].split('.')[-1]
        context['file_name'] = question.research_question.attachment.name.split("/")[-1]
        if self.request.user.researcheruser.status.status != "not_answered":
            context['answer'] = question.answer
            return context
        deadLine = question.hand_out_date + datetime.timedelta(days=+7)
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = deadLine - now
        context['day'] = delta.days
        context['hour'] = delta.seconds // 3600
        context['minute'] = (delta.seconds % 3600) // 60
        context['second'] = delta.seconds % 60
        return context

    def post(self, request, *args, **kwargs):
        researcherStatus = request.user.researcheruser.status
        if 'accelerator' in request.POST.keys() and researcherStatus.status != 'deactivated':
            if request.POST['accelerator'] == ACCELERATOR:
                researcherStatus.status = 'free'
                researcherStatus.save()
                return HttpResponseRedirect(reverse('researcher:index'))
        question = self.request.user.researcheruser.researchquestioninstance_set.all().reverse().first()
        uuid_id = question.research_question.uniqe_id
        deadLine = question.hand_out_date + datetime.timedelta(days=+7)
        now = datetime.datetime.now(datetime.timezone.utc)
        if now < deadLine:
            if 'answer' in request.FILES:
                question.answer = request.FILES['answer']
                question.is_answered = True
                subject = 'Research Question Validation'
                message = """با عرض سلام و خسته نباشید.
                پژوهشگر {} به نام {} به سوال پژوهشی {} پاسخ داده است.
                لطفا پاسخ پژوهشگر را ارزیابی نمایید.
                با تشکر""".format(self.request.user.username,
                                  self.request.user.researcheruser.researcherprofile.fullname,
                                  question.research_question.question_title)
                email = question.research_question.expert.user.username
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email, "a.jafarzadeh1998@gmail.com"],
                    )
                except TimeoutError:
                    return HttpResponse('Timeout Error!!')
                question.save()
                request.user.researcheruser.status.status = 'wait_for_result'
                request.user.researcheruser.status.save()
        return HttpResponseRedirect(reverse("researcher:question-show", kwargs={"question_id": uuid_id}))


@permission_required(('researcher.be_researcher', 'researcher.is_active'), login_url='/login/')
def ajax_Technique_review(request):
    form = forms.TechniqueReviewFrom(request.POST, request.FILES)
    if form.is_valid():
        description = form.cleaned_data['request_body']
        method = form.cleaned_data['request_confirmation_method']
        technique = request.user.researcheruser.techniqueinstance_set.all().filter(
            pk=request.POST['technique_id']).first()
        if method != "exam":
            resume = form.cleaned_data['new_resume']
            technique_review = models.TechniqueReview(technique_instance=technique, description=description,
                                                      method=method, resume=resume)
        else:
            technique_review = models.TechniqueReview(technique_instance=technique, description=description,
                                                      method=method)
        technique.level = None
        technique.save()
        technique_review.save()
        subject = 'Research Question Validation'
        message = """با عرض سلام و خسته نباشید.
        پژوهشگر {}  با نام کاربری {} در خواست ارتفا سطح تکنیک {} را از طریق {} داده است.
        لطفا درخواست وی را ارزیابی نمایید.
        با تشکر""".format(request.user.researcheruser.researcherprofile.fullname, request.user.username,
                          technique.technique.technique_title, method)
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
            )
        except TimeoutError:
            return HttpResponse('Timeout Error!!')
        data = {'success': 'successful'}
        return JsonResponse(data)
    return JsonResponse(form.errors, status=400)


@permission_required(('researcher.be_researcher', 'researcher.is_active'), login_url='/login/')
def ShowProject(request):
    project = Project.objects.filter(id=request.GET.get('id')).first()
    json_response = model_to_dict(project.project_form)
    json_response['deadline'] = 'نا مشخص'
    if project.status == 1 and project.date_project_started and project.date_phase_three_deadline:
        json_response['deadline'] = date_last(datetime.date.today(), project.date_phase_three_deadline)
    else:
        json_response['deadline'] = date_last(project.date_project_started, project.date_phase_three_deadline)
    json_response['submission_date'] = gregorian_to_numeric_jalali(project.date_submitted_by_industry)
    for ind, value in enumerate(json_response['key_words']):
        json_response['key_words'][ind] = value.__str__()
    json_response['required_technique'] = []
    for tech in project.project_form.required_technique:
        json_response['required_technique'].append(tech.__str__())
    projects_comments = project.get_comments()
    all_comments = projects_comments.exclude(researcher_user=None)
    json_response['comments'] = []
    for com in all_comments:
        try:
            url = com.attachment.url[com.attachment.url.find('media', 2):]
        except:
            url = "None"
        temp = {
            'pk': com.pk,
            'description': com.description,
            'replied_text': com.replied_text,
            'sender_type': com.sender_type,
            'attachment': url,
        }
        json_response['comments'].append(temp)
        if (com.sender_type == 'expert' or com.sender_type == 'system') and com.status == 'not_seen':
            com.status = 'seen'
            com.save()
    json_response['status'] = request.user.researcheruser.status.status
    return JsonResponse(json_response)


@permission_required(('researcher.be_researcher', 'researcher.is_active'), login_url='/login/')
def DeleteComment(request):
    try:
        comment = get_object_or_404(Comment, pk=request.POST['id'])
        comment.delete()
    except:
        return JsonResponse({}, 400)
    return JsonResponse({'successful': "successful"})


@permission_required(('researcher.be_researcher', 'researcher.is_active'), login_url='/login/')
def ApplyProject(request):
    if request.user.researcheruser.status.status == "waiting":
        data = {"error": "your waiting for another project"}
        return JsonResponse(data, status=400)
    form = forms.ApplyForm(request.POST)
    if form.is_valid():
        project = get_object_or_404(Project, id=request.POST['id'])
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
        return JsonResponse(data={'success': "success"})
    return JsonResponse(form.errors, status=400)


@permission_required(('researcher.be_researcher', 'researcher.is_active'), login_url='/login/')
def MyProject(request):
    project = Project.objects.filter(id=request.GET.get('id')).first()
    json_response = model_to_dict(project.project_form)
    json_response['deadline'] = 'نا مشخص'
    if project.status == 1 and project.date_project_started and project.date_phase_three_deadline:
        json_response['deadline'] = date_last(datetime.date.today(), project.date_phase_three_deadline)
    else:
        json_response['deadline'] = date_last(project.date_project_started, project.date_phase_three_deadline)
    json_response['submission_date'] = gregorian_to_numeric_jalali(project.date_submitted_by_industry)
    for ind, value in enumerate(json_response['key_words']):
        json_response['key_words'][ind] = value.__str__()
    json_response['required_technique'] = []
    for tech in project.project_form.required_technique:
        json_response['required_technique'].append(tech.__str__())
    all_comments = project.get_comments().exclude(researcher_user=None)
    json_response['comments'] = []
    for com in all_comments:
        try:
            url = com.attachment.url[com.attachment.url.find('media', 2):]
        except:
            url = "None"
        temp = {
            'pk': com.pk,
            'description': com.description,
            'replied_text': com.replied_text,
            'sender_type': com.sender_type,
            'attachment': url
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

@permission_required(('researcher.be_researcher', 'researcher.is_active'), login_url='/login/')
def AddComment(request):
    form = forms.CommentForm(request.POST, request.FILES)
    project = Project.objects.filter(id=request.POST['project_id'])[0]
    if form.is_valid():
        description = form.cleaned_data['description']
        attachment = form.cleaned_data['attachment']
        comment = Comment(description=description
                          , attachment=attachment
                          , project=project
                          , researcher_user=request.user.researcheruser
                          , expert_user=project.expert_accepted
                          , sender_type="researcher"
                          , status='unseen')
        comment.save()
        if attachment is not None:
            url = comment.attachment.url[comment.attachment.url.find('media', 2):]
            data = {
                'success': 'successful',
                'attachment': url,
                'description': description,
                'pk': comment.pk,
            }
        else:
            data = {
                'success': 'successful',
                'attachment': "None",
                'description': description,
                'pk': comment.pk,
            }
        return JsonResponse(data)
    return JsonResponse(form.errors, status=400)


@permission_required('researcher.be_researcher', login_url='/login/')
def DeleteScientificRecord(request):
    try:
        sci_rec = get_object_or_404(models.ScientificRecord, pk=request.POST['pk'])
    except:
        return JsonResponse({"errors": "Scientific record isn't found"}, status=400)
    sci_rec.delete()
    return JsonResponse({"successfull": "Scientific record is deleted"})


@permission_required('researcher.be_researcher', login_url='/login/')
def DeleteExecutiveRecord(request):
    try:
        exe_rec = get_object_or_404(models.ExecutiveRecord, pk=request.POST['pk'])
    except:
        return JsonResponse({"errors": "Executive record isn't found"}, status=400)
    exe_rec.delete()
    return JsonResponse({"successfull": "Executive record is deleted"})


@permission_required('researcher.be_researcher', login_url='/login/')
def DeleteStudiousRecord(request):
    try:
        stu_rec = get_object_or_404(models.StudiousRecord, pk=request.POST['pk'])
    except:
        return JsonResponse({"errors": "Studious record isn't found"}, status=400)
    stu_rec.delete()
    return JsonResponse({"successfull": "Studious record is deleted"})


@permission_required([], login_url='/login/')
def show_resume_preview(request):
    researcherProfile = models.ResearcherProfile.objects.get(id=request.GET.get('id'))
    researcher = researcherProfile.researcher_user
    # TODO: Plz check resume key when it is none! I[ Reza :) ] comment that because of error type 500
    researcher_information = {
        'photo': researcherProfile.photo.url,
        'name': researcherProfile.__str__(),
        'major': researcherProfile.major,
        'grade': researcherProfile.grade,
        'university': researcherProfile.university,
        'entry_year': researcherProfile.entry_year,
        # 'resume': researcherProfile.resume.url,
        'techniques': [],
        'scientific_record': serialize('json', models.ScientificRecord.objects.filter(
            researcherProfile=researcherProfile)),
        'executive_record': serialize('json', models.ExecutiveRecord.objects.filter(
            researcherProfile=researcherProfile)),
        'research_record': serialize('json', models.StudiousRecord.objects.filter(researcherProfile=researcherProfile)),
    }
    for tech in models.TechniqueInstance.objects.filter(researcher=researcher):
        researcher_information['techniques'].append(tech.technique.technique_title)
    project = get_object_or_404(Project, pk=request.GET["project_id"])
    comments = []
    comment_list = project.comment_set.all().filter(researcher_user=researcher).exclude(sender_type='system')
    for comment in comment_list:
        try:
            url = get_url(comment.attachment.url)
        except:
            url = "None"
        comments.append({
            'id': comment.id,
            'text': comment.description,
            'sender_type': comment.sender_type,
            'attachment': url,
            'pk': comment.pk,
        })
        if comment.sender_type == 'researcher':
            comment.status = 'seen'
            comment.save()
    researcher_information['comments'] = comments
    return JsonResponse(researcher_information)

def checkUserId(request, userId):
    if models.ResearcherUser.objects.filter(userId=userId).count():
        return False
    return True

TECHNIQUES = {
    'Polymerase Chain Reaction': 'Molecular Biology',
    'RNA-Seq': 'Molecular Biology',
    'DNA Metylation Analysis': 'Molecular Biology',
    'DNA Gel Electorphoresis': 'Molecular Biology',
    'Two-Dimensional Gel Electorphoresis': 'Molecular Biology',
    'Gel Purification': 'Molecular Biology',
    'DNA Ligation Reaction': 'Molecular Biology',
    'Restriction Enzyme Digests': 'Molecular Biology',
    'Bacterial Culture': 'Molecular Biology',
    'Bacterial Transformation The Heat Shock Method': 'Molecular Biology',
    'Bacterial Transformation Electroporation': 'Molecular Biology',
    'Plasmid Purification': 'Molecular Biology',
    'The Western Bolt': 'Molecular Biology',
    'The Northern Bolt': 'Molecular Biology',
    'Co-Immunoprecipition and Pull-Down Assays': 'Molecular Biology',
    'Expression Profiling with Microarrays': 'Molecular Biology',
    'Cytogenetics': 'Molecular Biology',
    'Chromatin Immunoprecipition': 'Molecular Biology',
    'Recombineering and Gene Targeting': 'Molecular Biology',
    'SNP Genotyping': 'Molecular Biology',
    'Genome Editing': 'Molecular Biology',
    'Gene Silencing': 'Molecular Biology',

    'The ELISA Method': 'Immunology',
    'Flow Cytometry': 'Immunology',
    'Flow cell storing': 'Immunology',
    'Magnetice Bead cell Isolation': 'Immunology',

    'SEM Imaging of Biological Samples': 'Imaging',
    'Biodistribution of Nano-drog Carriers Applications of SEM': 'Imaging',
    'Imaging of Biological Samples with Optical and Confocal Microscopy': 'Imaging',
    'Calcium Imaging in Neurons': 'Imaging',
    'Animal Flourescene': 'Imaging',
    'Animal CT': 'Imaging',
    'Animal MRI': 'Imaging',
    'Animal SPECT': 'Imaging',
    'Animal PET': 'Imaging',
    'Animal US': 'Imaging',

    'Sterile Tissue Harvest': 'Histology',
    'Diagnostic Necropsy and Tissue Harvest': 'Histology',
    'Tissue Cryopreservation': 'Histology',
    'Tissue Fixation': 'Histology',
    'Microtome Sectioning': 'Histology',
    'Cryostat Sectioning': 'Histology',
    'H&E staining': 'Histology',
    'Histochemistry': 'Histology',
    'Histoflouresence': 'Histology',

    'An Introduction to the Centrifuge': 'General Lab',
    'Regulating Temperature in the Lab Preserving Samples Using Cold': 'General Lab',
    'Introduction to the Bunsen Burner': 'General Lab',
    'Introduction to Serological Pipettes and Pipettor': 'General Lab',
    'An Introduction to the Micropipettor': 'General Lab',
    'Making Solutions in the Laboratory': 'General Lab',
    'Understanding Concentration and Measuring Volumes': 'General Lab',
    'Introduction to the Microplate Reader': 'General Lab',
    'Regulation Temperature in the Lab Applying Heat': 'General Lab',
    'Common Lab Glassware and Users': 'General Lab',
    'Solutions and Concentrations': 'General Lab',
    'Determining the Density of a Solid and Liquid': 'General Lab',
    'Determining the Mass Percent Composition in an Aqueous Solution': 'General Lab',
    'Determining the Empirical Formula': 'General Lab',
    'Determining the Solubility Rules of Ionic Compounds': 'General Lab',
    'Using a pH Meter': 'General Lab',
    'Introduction to Titration': 'General Lab',
    'Ideal Gas Law': 'General Lab',

    'An Introduction to Working in Hood': 'Lab Safety',
    'Operation of High-pressure Reactor Vessels': 'Lab Safety',
    'Decontamination for laboratory Biosafety Proper Waste Disposal': 'Lab Safety',
    'Fume Hoods and Laminar Flow Cabinates': 'Lab Safety',
    'Handling Chemical Spills': 'Lab Safety',
    'Chemical Storage Categories,Hazards and Compatibilies': 'Lab Safety',
    'Guidelines in Case of an Laboratory Emergency': 'Lab Safety',
    'Work with Hot and Cold Sources': 'Lab Safety',
    'Electrical Safety': 'Lab Safety',
    'Emergency Eyewash and Shower Stations': 'Lab Safety',
    'Proper Personal Protective Equipment': 'Lab Safety',

    'Serearching on articles resources': 'Research Methodology',
    'Endnote': 'Research Methodology',
    'spss/graph pad': 'Research Methodology',
    'Essy writing': 'Research Methodology',
    'Poster Presentation': 'Research Methodology',
    'Microsoft Office': 'Research Methodology',
    'Photoshop': 'Research Methodology',

    'Introduction to the Spectrophotometer': 'Biochemistry',
    'Measuring Mass in the Laboratory': 'Biochemistry',
    'NMR': 'Biochemistry',
    'X-ray Fluorescence(XRF)': 'Biochemistry',
    'Gas Chromatography(GC) with Flame-lonization Detection': 'Biochemistry',
    'High-Performance Liquid Chromatography(HPLC)': 'Biochemistry',
    'Ion-Exchange Chromatography': 'Biochemistry',
    'Chromatography-based Biomolecule Purification Methods': 'Biochemistry',
    'Capillary Electrophoresis(CE)': 'Biochemistry',
    'Introduce to Mass Spectrometry': 'Biochemistry',
    'Scanning Electron Microscopy(SEM)': 'Biochemistry',
    'Cyclic Voltammetry(CV)': 'Biochemistry',
    'MALDI-TOF Mass Spectrometry': 'Biochemistry',
    'Tandem Mass Spectrometry': 'Biochemistry',
    'Protein Crystallization': 'Biochemistry',
    'Electrophoretic Mobility Shift Assay(EMSA)': 'Biochemistry',
    'Photometric Protein Determination': 'Biochemistry',
    'Density Gradient Ultracentrifugation': 'Biochemistry',
    'Forster Resonance Energy Transfer(FRET)': 'Biochemistry',
    'Surface Plasmon Resonance(SPR)': 'Biochemistry',
    'Synthetic Organic Chemestry': 'Biochemistry',

    'An Introduction to the Laboratory Mouse Mos Musculus': 'Animal Lab',
    'Rodent Handling and Restraint Techniques': 'Animal Lab',
    'Basic Mouse Care and Maintenance': 'Animal Lab',
    'Development and Reproduction of the Laboratory Mouse': 'Animal Lab',
    'Basic Care Procedures': 'Animal Lab',
    'Fundamentals of Breeding and Weaning': 'Animal Lab',
    'Rodent Identification I': 'Animal Lab',
    'Rodent Identification II': 'Animal Lab',
    'Compound Administration I': 'Animal Lab',
    'Compound Administration II': 'Animal Lab',
    'Compound Administration III': 'Animal Lab',
    'Compound Administration IV': 'Animal Lab',
    'Blood Withdrawal I': 'Animal Lab',
    'Anesthesia Introduction and Maintenance': 'Animal Lab',
    'Rodent Stereoxtic Surgery': 'Animal Lab',
    'Considerations for Rodent Surgery': 'Animal Lab',

    'Whole-Mount in Situ Hybridization': 'Cellular Biology',
    'Molecular Cloning': 'Cellular Biology',
    'Yeast Transformation and Cloning': 'Cellular Biology',
    'Embryonic Steam Cell Culture and Differentiaton': 'Cellular Biology',
    'An Introduction to Transfection': 'Cellular Biology',
    'Transduction': 'Cellular Biology',
    'Introduction to Light Microscopy': 'Cellular Biology',
    'Introduction to Fluorescence Microscopy': 'Cellular Biology',
    'Histological Sample Preparation for Light Microscopy': 'Cellular Biology',
    'Cell-surface Biotinylation Assay': 'Cellular Biology',
}


# 7072488c-02ab-4362-9e51-7100dae78473
# persiontools

def forbidden_access(request):
    return render(request, 'researcher/forbid_access.html', {})
