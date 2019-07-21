from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views import generic
from django.contrib.auth.models import User

from . import models ,forms


class Index(generic.FormView):
    template_name = 'researcher/layouts/initial_information.html'
    form_class = forms.InitailForm

    def get(self, request, *args, **kwargs):
        try:
            researcher = get_object_or_404(models.ResearcherUser ,user=request.user)
        except:
            return HttpResponseRedirect(reverse('chamran:login'))
        if researcher.researcherstatus.status == 'signed_up':
            return super().get(request, *args, **kwargs)
        return render(request ,'researcher/index.html')
    
    def post(self ,request ,*args, **kwargs):
        form = forms.InitailForm(request.POST ,request.FILES)
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

            researcher = get_object_or_404(models.ResearcherUser ,user=request.user)

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
            researcher_status = researcher.researcherstatus
            researcher_status.status = 'free'
            researcher_status.save()
            return HttpResponseRedirect(reverse('researcher:index'))
        return super().post(self ,request ,*args, **kwargs)

class userInfo(generic.TemplateView):
    template_name = 'researcher/userInfo.html'


class Login(generic.TemplateView):
    template_name = 'registration/base.html'


class UserPass(generic.TemplateView):
    template_name = 'registration/user_pass.html'
