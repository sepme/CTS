from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, Http404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

import os

from . import models
from . import forms


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
            status.status = 'free'
            status.save()
            print(researcher_profile)
            return HttpResponseRedirect(reverse('researcher:index'))

        return super().post(self, request, *args, **kwargs)


class UserInfo(generic.FormView):
    template_name = 'researcher/userInfo.html'
    form_class = forms.ResearcherProfileForm

    def get(self, request, *args, **kwargs):
        if (not request.user.is_authenticated) or (not models.ResearcherUser.objects.filter(user=request.user).count()):
            return HttpResponseRedirect(reverse('chamran:login'))
        context = {
                    'form' :  forms.ResearcherProfileForm(self.request.user,
                                           instance=self.request.user.researcheruser.researcherprofile,
                                           initial={
                                                'grade':
                                                    self.request.user.researcheruser.researcherprofile.grade,
                                                'email':
                                                    self.request.user.username})
                    }
        return render(request ,'researcher/userInfo.html' ,context=context)
        # return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] =  forms.ResearcherProfileForm(self.request.user,
                                           instance=self.request.user.researcheruser.researcherprofile,
                                           initial={
                                               'grade':
                                                   self.request.user.researcheruser.researcherprofile.grade,
                                                'email':
                                                    self.request.user.username})
        return context

    def post(self, request, *args, **kwargs):
        print('--------------------------------')
        form = forms.ResearcherProfileForm(self.request.user ,request.POST, request.FILES,
                                        #    initial={
                                        #        'grade':
                                        #            self.request.user.researcheruser.researcherprofile.grade})
        )
        print(self.request.POST)
        if form.is_valid():
            profile = request.user.researcheruser.researcherprofile
            if profile.photo:
                if os.path.isfile(profile.photo.path):
                    os.remove(profile.photo.path)
                profile.photo = form.cleaned_data['photo']
            else:
                profile.photo = form.cleaned_data['photo']
                print(profile.photo)
            print(profile.photo)
            profile.address = form.cleaned_data['address']
            profile.email = form.cleaned_data['email']
            profile.home_number = form.cleaned_data['home_number']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.grade = form.cleaned_data['grade']
            profile.team_work = form.cleaned_data['team_work']
            profile.creative_thinking = form.cleaned_data['creative_thinking']
            profile.interest_in_major = form.cleaned_data['interest_in_major']
            profile.motivation = form.cleaned_data['motivation']
            profile.sacrifice = form.cleaned_data['sacrifice']
            profile.diligence = form.cleaned_data['diligence']
            profile.interest_in_learn = form.cleaned_data['interest_in_learn']
            profile.punctuality = form.cleaned_data['punctuality']
            profile.data_collection = form.cleaned_data['data_collection']
            profile.project_knowledge = form.cleaned_data['project_knowledge']
            profile.description = form.cleaned_data['description']

            profile.save()
            return HttpResponseRedirect(reverse("researcher:index"))
        context = {
                    'form' :  forms.ResearcherProfileForm(self.request.user,
                                           instance=self.request.user.researcheruser.researcherprofile,
                                           initial={
                                               'grade':
                                                   self.request.user.researcheruser.researcherprofile.grade,}),
                    }

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
            'success' : 'success',
        }
        return JsonResponse(data)
    else:
        return JsonResponse(form.errors)

def ajax_ExecutiveRecord(request):
    form = forms.ExecutiveRecordForm(request.POST)
    if form.is_valid():
        executive_record = form.save(commit=False)
        executive_record.researcherProfile = request.user.researcheruser.researcherprofile
        executive_record.save()
        data = {
            'success' : 'success',
        }
        return JsonResponse(data)
    else:
        return JsonResponse(form.errors)

def ajax_StudiousRecord(request):
    form = forms.StudiousRecordForm(request.POST)
    if form.is_valid():
        studious_record = form.save(commit=False)
        studious_record.researcherProfile = request.user.researcheruser.researcherprofile
        studious_record.save()
        data = {
            'success' : 'success',
        }
        return JsonResponse(data)
    else:
        return JsonResponse(form.errors)

def signup(request, username):
    user = get_object_or_404(User, username=username)
    researcher = models.ResearcherUser(user=user)
    researcher.save()
    return HttpResponseRedirect(reverse('researcher:index'))


class Messages(generic.TemplateView):
    template_name = 'researcher/messages.html'

class Technique(generic.TemplateView):
    template_name = 'researcher/technique.html'

class Question(generic.TemplateView):
    template_name = 'researcher/question.html'
