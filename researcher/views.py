from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, Http404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

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
        # form = forms.InitialInfoForm(request.FILES, request.POST)
        print(form.is_valid())
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

    def post(self, request, *args, **kwargs):
        print('--------------------------------')
        print(request.POST)
        form = forms.ResearcherProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print('form validated!!!!!!!!!')
            profile = request.user.researcheruser.researcherprofile

            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.major = form.cleaned_data['major']
            profile.national_code = form.cleaned_data['national_code']
            profile.grade = form.cleaned_data['grade', 'university']
            profile.entry_year = form.cleaned_data['entry_year']
            profile.student_number = form.cleaned_data['student_number']
            profile.address = form.cleaned_data['address']
            profile.home_number = form.cleaned_data['home_number']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.email = form.cleaned_data['email']
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
        return super().post(self, request, *args, **kwargs)


def signup(request, username):
    user = get_object_or_404(User, username=username)
    researcher = models.ResearcherUser(user=user)
    researcher.save()
    return HttpResponseRedirect(reverse('researcher:index'))


class Messages(generic.TemplateView):
    template_name = 'researcher/messages.html'
