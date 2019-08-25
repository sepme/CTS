from django.core.exceptions import ValidationError
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from . import models
from . import forms


class Index(generic.TemplateView):
    template_name = 'industry/index.html'
    industry = models.IndustryUser

    def get(self, request, *args, **kwargs):
        try:
            self.industry = get_object_or_404(models.IndustryUser, user=request.user)
        except:
            return HttpResponseRedirect(reverse('chamran:login'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry'] = self.industry
        if self.request.user.industryuser.first_login:
            context['form'] = forms.IndustryBasicInfoForm(self.request.user)
        try:
            if self.industry.industryform:
                context['photo'] = self.industry.industryform.photo
        except:
            context['basic_info'] = True
        return context

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
            industry_info = models.IndustryForm(photo=photo,
                                                name=name,
                                                registration_number=registration_number,
                                                date_of_foundation=date_of_foundation,
                                                research_field=research_field,
                                                industry_type=industry_type,
                                                industry_address=industry_address,
                                                phone_number=phone_number,
                                                email_address=email_address)
            industry_info.save()
            industry_user.first_login = False
            industry_user.industryform = industry_info
            industry_user.save()
            return HttpResponseRedirect(reverse('industry:index'))
        return render(request, 'industry/index.html', context={'form': form})


class userInfo(generic.FormView):
    template_name = 'industry/userInfo.html'
    form_class = forms.IndustryInfoForm
    industry = models.IndustryUser

    def get(self, request, *args, **kwargs):
        try:
            self.industry = get_object_or_404(models.IndustryUser, user=request.user)
        except:
            return HttpResponseRedirect(reverse('chamran:login'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo'] = self.industry.industryform.photo
        return context

    def post(self, request, *args, **kwargs):
        form = forms.IndustryInfoForm(request.POST, request.FILES)
        if form.is_valid():
            industry_form = request.user.industryuser.industryform
            industry_form.name = form.cleaned_data['name']
            industry_form.photo = form.cleaned_data['photo']
            industry_form.registration_number = form.cleaned_data['registration_number']
            industry_form.date_of_foundation = form.cleaned_data['date_of_foundation']
            industry_form.research_field = form.cleaned_data['research_field']
            industry_form.industry_type = form.cleaned_data['industry_type']
            industry_form.industry_address = form.cleaned_data['industry_address']
            industry_form.phone_number = form.cleaned_data['phone_number']
            industry_form.email_address = form.cleaned_data['email_address']
            industry_form.awards_honors = form.cleaned_data['awards_honors']
            industry_form.tax_declaration = form.cleaned_data['tax_declaration']

            industry_form.save()
            return HttpResponseRedirect(reverse('industry:index'))
        return super().post(request, *args, **kwargs)


class newProject(generic.FormView):
    template_name = 'industry/newProject.html'
    form_class = forms.ProjectForm
    industry = models.IndustryUser

    def get(self, request, *args, **kwargs):
        try:
            self.industry = get_object_or_404(models.IndustryUser, user=request.user)
        except:
            return HttpResponseRedirect(reverse('chamran:login'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry'] = self.industry
        if self.industry.industryform:
            context['photo'] = self.industry.industryform.photo
        return context

    def post(self, request, *args, **kwargs):
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            # 'required_technique'
            project_title_persian = form.cleaned_data['project_title_persian']
            project_title_english = form.cleaned_data['project_title_english']
            # key_words = form.cleaned_data['key_words']
            research_methodology = form.cleaned_data['research_methodology']
            main_problem_and_importance = form.cleaned_data['main_problem_and_importance']
            predict_profit = form.cleaned_data['predict_profit']
            required_lab_equipment = form.cleaned_data['required_lab_equipment']
            innovation = form.cleaned_data['innovation']
            approach = form.cleaned_data['approach']
            policy = form.cleaned_data['policy']
            required_budget = form.cleaned_data['required_budget']
            project_phase = form.cleaned_data['project_phase']

            new_project_form = models.ProjectForm(project_title_persian=project_title_persian,
                                                  project_title_english=project_title_english,
                                                  research_methodology=research_methodology,
                                                  main_problem_and_importance=main_problem_and_importance,
                                                  predict_profit=predict_profit,
                                                  required_lab_equipment=required_lab_equipment,
                                                  innovation=innovation,
                                                  approach=approach,
                                                  policy=policy,
                                                  required_budget=required_budget,
                                                  project_phase=project_phase,
                                                  )
            new_project_form.save()
            new_project = models.Project(project_form=new_project_form, industry_creator=request.user.industryuser)
            new_project.save()
            return HttpResponseRedirect(reverse('industry:project_list'))
        return super().post(request, args, kwargs)


class ProjectListView(generic.ListView):
    template_name = 'industry/project_list.html'
    model = models.ProjectForm

    def get(self, request, *args, **kwargs):
        try:
            self.industry = get_object_or_404(models.IndustryUser, user=request.user)
        except:
            return HttpResponseRedirect(reverse('chamran:login'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry'] = self.industry
        if self.industry.industryform:
            context['photo'] = self.industry.industryform.photo
        return context


class UserInfo(generic.TemplateView):
    template_name = 'industry/userInfo.html'


class NewProject(generic.TemplateView):
    template_name = 'industry/newProject.html'

class Messages(generic.TemplateView):
    template_name = 'industry/messages.html'