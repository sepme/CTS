from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views import generic
from django.contrib.auth.models import User

from . import models
from . import forms


class Index(generic.FormView):
    template_name = 'researcher/layouts/initial_information.html'
    form_class = forms.InitailForm

    def get(self, request, *args, **kwargs):
        try:
            self.researcher = get_object_or_404(models.ResearcherUser, user=request.user)
        except:
            return HttpResponseRedirect(reverse('chamran:login'))
        print(self.researcher.status.status)
        if self.researcher.status.status == 'signed_up':
            return super().get(request, *args, **kwargs)
        return render(request, 'researcher/index.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['researcheruser'] = self.researcher
        return context

    def post(self, request, *args, **kwargs):
        form = forms.InitailForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            photo = form.cleaned_data['photo']
            address = form.cleaned_data['address']
            national_code = form.cleaned_data['national_code']
            entry_year = form.cleaned_data['entry_year']
            grade = form.cleaned_data['grade']
            university = form.cleaned_data['university']
            major = form.cleaned_data['major']
            home_number = form.cleaned_data['home_number']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            student_number = form.cleaned_data['student_number']

            researcher = get_object_or_404(models.ResearcherUser, user=request.user)

            profile = models.ResearcherProfile(
                researcher_user=researcher,
                first_name=first_name,
                last_name=last_name,
                photo=photo,
                address=address,
                national_code=national_code,
                entry_year=entry_year,
                grade=grade,
                university=university,
                major=major,
                home_number=home_number,
                phone_number=phone_number,
                email=email,
                student_number=student_number
            )
            profile.save()
            researcher_status = researcher.status
            researcher_status.status = 'free'
            researcher_status.save()
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


class Login(generic.TemplateView):
    template_name = 'registration/login.html'


class UserPass(generic.TemplateView):
    template_name = 'registration/user_pass.html'


def signup(request, username):
    user = get_object_or_404(User, username=username)
    researcher = models.ResearcherUser(user=user)
    researcher.save()
    return HttpResponseRedirect(reverse('researcher:index'))
