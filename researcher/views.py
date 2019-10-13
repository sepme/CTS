from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, Http404 ,HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import os ,random ,datetime

from . import models
from . import forms
from expert.models import ResearchQuestion


class Index(LoginRequiredMixin, generic.FormView):
    template_name = 'researcher/index.html'
    form_class = forms.InitialInfoForm
    login_url = '/login/'

    # def get(self, request, *args, **kwargs):
    # #     try:
    # #         self.researcher = get_object_or_404(models.ResearcherUser, user=request.user)
    # #     except:
    # #         return HttpResponseRedirect(reverse('chamran:login'))
    # #     # print(self.researcher.status.status)
    # #     # if self.researcher.status.status == 'signed_up':
    # #     #     return super().get(request, *args, **kwargs)
    #     return render(request, 'researcher/index.html', self.get_context_data())

    def get(self, request, *args, **kwargs):
        try:
            models.ResearcherUser.objects.get(user=request.user)
        except models.ResearcherUser.DoesNotExist:
            raise Http404('.کاربر پژوهشگر مربوطه یافت نشد')
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        if self.request.user.researcheruser.researchquestioninstance_set.all().count() > 0:
            context['question_instance'] = "True"
            context['uuid'] = self.request.user.researcheruser.researchquestioninstance_set.all().reverse()[0].research_question.uniqe_id
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
        print(self.request.POST)
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
    technique = {"Sterile Tissue Harvest" : "histology",
                 "Diagnostic Necropsy and Tissue Harvest" : "histology",
                 "Tissue Cryopreservation" : "histology",
                 "Tissue Fixation" : "histology",
                 "Microtome Sectioning" : "histology",
                 "Cryostat Sectioning" : "histology",
                 "H&E staining" : "histology",
                 "Histochemistry" : "histology",
                 "Histoflouresence" : "histology",

                 "An Introduction to the Centrifuge" : "general lab",
                 "Regulating Temperature in the Lab Preserving Sample Using Cold" : "general lab",
                 "Introduction to the Bunsen Burner" : "general lab",
                 "Introduction to Serological Pipettes and Pipettor" : "general lab",
                 "An Introduction to the Micropipettor" : "general lab",
                 "Making Solutions in the Laboratory" : "general lab",
                 "Understanding Concentration and Measuring Volums" : "general lab",
                 "Introduction to the Microplate Reader" : "general lab",
                 "Regulation Temperature in the Lab Applying Heat" : "general lab",
                 "Common Lab Glassware and Users" : "general lab",
                 "Solutions and Concentrations" : "general lab",
                 "Determining the Density of a Solid and Liquid" : "general lab",
                 "Determining the Mass Percent Composition in an Aqueous Solution" : "general lab",
                 "Determining the Empirical Formula" : "general lab",
                 "Determining the Solubility Rules of Ionic Compounds" : "general lab",
                 "Using a pH Meter" : "general lab",
                 "Introduction to Titration" : "general lab",
                 "Ideal Gas Law" : "general lab",
                }

    def post(self ,request ,*args, **kwargs):
        print(self.request.POST)
        technique_title = request.POST['technique-name']
        method = request.POST['confirmation_method']
        resume = request.FILES['resume']

        subject = 'Technique Validation'
        message ="""کاربر به نام کاربری {} و به نام {} {} ، تکنیک {} را افزوده است.
        برای ارزیابی گزینه {} را انتخاب کرده است. لطفا {}را ارزیابی کنید و نتیجه را اعلام کنید.
        با تشکر""".format(self.request.user.username ,self.request.user.researcheruser.researcherprofile.fist_name ,self.request.user.researcheruser.researcherprofile.last_name,
                            technique_title ,method ,self.request.user.username)
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False
            )
        except TimeoutError:
            return HttpResponse('Timeout Error!!')
        cat_technique = self.technique_list[technique_title]
        # technique_title = models.Technique
        #blah blah
        return HttpResponseRedirect(reverse("researcher:technique"))

class Question(generic.TemplateView):
    template_name = 'researcher/question.html'

    def get(self, request, *args, **kwargs):
        try:
           researcher = models.ResearcherUser.objects.get(user=request.user)
        except models.ResearcherUser.DoesNotExist:
            raise Http404('.کاربر پژوهشگر مربوطه یافت نشد')
        if (not request.user.is_authenticated) or (not models.ResearcherUser.objects.filter(user=request.user).count()):
            return HttpResponseRedirect(reverse('chamran:login'))
        if researcher.status.status == 'not_answered':
            if researcher.researchquestioninstance_set.all().count():
                question = self.request.user.researcheruser.researchquestioninstance_set.all().reverse()[0]
                return HttpResponseRedirect(reverse('researcher:question-show' ,kwargs={'question_id' : question.research_question.uniqe_id}))
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
        question_list = ResearchQuestion.objects.filter(is_answered=False)
        print(len(question_list))
        print(random.randint(1 ,len(question_list)))
        question = question_list[random.randint(1 ,len(question_list))-1]
        question_instance = models.ResearchQuestionInstance(research_question=question,
                                                            researcher = request.user.researcheruser)
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
                pass #show its in waiting for evaliator answer
            if question.is_correct :
                request.user.researcheruser.status.status = 'free'
                request.user.researcheruser.status.status.save()
                #show massage that u have answered
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
        if deltatime.days < 8:
            context['rest_days'] = 8 - deltatime.days
        context['question_title'] = question.research_question.question_title
        context['question'] = question.research_question.question
        context['attach_file'] = question.research_question.attach_file
        context['hour'] = datetime.datetime.now().hour
        context['minute'] = datetime.datetime.now().minute
        context['second'] = datetime.datetime.now().second
        return context
    
    def post(self ,request ,*args, **kwargs):
        question = self.request.user.researcheruser.researchquestioninstance_set.all().reverse()[0]
        uuid_id = question.research_question.uniqe_id
        question.answer = request.FILES['answer']
        question.is_answered = True
        question.save()
        subject = 'Research Question Validation'
        message ="""با عرض سلام و خسته نباشید.
        پژوهشگر {} به نام {} {} به سوال پژوهشی شما پاسخ داده است.
        لطفا پاسخ پژوهشگر را ارزیابی نمایید.
        با تشکر""".format(self.request.user.username ,self.request.user.researcheruser.researcherprofile.first_name,
                          self.request.user.researcheruser.researcherprofile.last_name)
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
    print(request.POST)
    print(request.FILES)
    discription = request.POST['request_body']
    method = request.POST['request_confirmation_method']

    if discription is not None and method is not None:
        if method != "exam":
            resume = request.FILES['resume']
            if resume is None:
                data = {
                        'resume' : "حتما باید فایلی آپلود کنید.",
                    }
                return JsonResponse(data ,status=400)
            technique_review = models.TechniqueReview(technique = blah,discription=discription,
                                                      method=method ,resume=resume)
        else:
            technique_review = models.TechniqueReview(technique = blah,discription=discription,
                                                      method=method)
        technique_review.save()
        data = {'success' : 'successful'}
        return JsonResponse(data)

# 7072488c-02ab-4362-9e51-7100dae78473
#persiontools