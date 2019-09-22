import os
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.views import generic, View
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from ChamranTeamSite import settings
from industry.models import IndustryForm
from . import models
from . import forms


class Index(generic.TemplateView):
    template_name = 'industry/index.html'

    def get(self, request, *args, **kwargs):
        if (not request.user.is_authenticated) or (not models.IndustryUser.objects.filter(
                user=request.user).count()):
            return HttpResponseRedirect(reverse('chamran:login'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and \
                models.IndustryUser.objects.filter(user=self.request.user).count() and \
                self.request.user.industryuser.status == 'signed_up':
            context['form'] = forms.IndustryBasicInfoForm(self.request.user)
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
            if not industry_info.photo:
                with open(os.path.join(settings.BASE_DIR, 'industry/static/industry/img/profile.jpg'),
                          'rb') as image_file:
                    default_image = image_file.read()
                    industry_info.photo.save('profile.jpg', ContentFile(default_image))
            industry_user.status = 'free'
            industry_user.industryform = industry_info
            industry_user.save()
            return HttpResponseRedirect(reverse('industry:index'))
        return render(request, 'industry/index.html', context={'form': form})


class UserInfo(View):
    def get(self, request):
        if (not request.user.is_authenticated) or (not models.IndustryUser.objects.filter(user=request.user).count()):
            return HttpResponseRedirect(reverse('chamran:login'))
        context = {
            'form': forms.IndustryInfoForm(self.request.user,
                                           instance=self.request.user.industryuser.industryform,
                                           initial={
                                               'industry_type':
                                                   self.request.user.industryuser.industryform.industry_type})
        }
        return render(request, 'industry/userInfo.html', context=context)

    def post(self, request):
        form = forms.IndustryInfoForm(self.request.user, request.POST, request.FILES,
                                      initial={
                                          'industry_type': self.request.user.industryuser.industryform.industry_type})
        if form.is_valid():
            model_form = form.save(commit=False)
            IndustryForm.objects.filter(name=model_form.name).update(
                industry_type=model_form.industry_type,
                tax_declaration=model_form.tax_declaration,
                services_products=model_form.services_products,
                awards_honors=model_form.awards_honors
            )
            if request.user.industryuser.industryform.photo:
                os.remove(os.path.join(settings.MEDIA_ROOT, request.user.industryuser.industryform.name,
                                       request.user.industryuser.industryform.photo.name))
            if model_form.photo:
                model_form.photo.save(model_form.photo.name, model_form.photo)
                IndustryForm.objects.filter(name=model_form.name).update(photo=model_form.photo)
            else:
                with open(os.path.join(settings.BASE_DIR, 'industry/static/industry/img/profile.jpg'),
                          'rb') as image_file:
                    default_image = image_file.read()
                    model_form.photo.save('profile.jpg', ContentFile(default_image))
            return HttpResponseRedirect(reverse('industry:index'))
        return render(request, 'industry/userInfo.html', context={'form': form})


class NewProject(View):
    def get(self, request):
        if request.user.is_authenticated and (not models.IndustryUser.objects.filter(user=request.user).count()):
            return HttpResponseRedirect(reverse('chamran:login'))
        return render(request, 'industry/newProject.html', context={'form': forms.ProjectForm()})

    def post(self, request):
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            project_title_persian = form.cleaned_data['project_title_persian']
            project_title_english = form.cleaned_data['project_title_english']
            research_methodology = form.cleaned_data['research_methodology']
            main_problem_and_importance = form.cleaned_data['main_problem_and_importance']
            predict_profit = form.cleaned_data['predict_profit']
            required_lab_equipment = form.cleaned_data['required_lab_equipment']
            approach = form.cleaned_data['approach']
            policy = form.cleaned_data['policy']
            required_budget = form.cleaned_data['required_budget']
            project_phase = form.cleaned_data['project_phase']
            required_technique = form.cleaned_data['required_technique']
            progress_profitability = form.cleaned_data['progress_profitability']
            potential_problems = form.cleaned_data['potential_problems']
            new_project_form = models.ProjectForm(project_title_persian=project_title_persian,
                                                  project_title_english=project_title_english,
                                                  research_methodology=research_methodology,
                                                  main_problem_and_importance=main_problem_and_importance,
                                                  predict_profit=predict_profit,
                                                  required_lab_equipment=required_lab_equipment,
                                                  required_technique=required_technique,
                                                  approach=approach,
                                                  policy=policy,
                                                  required_budget=required_budget,
                                                  project_phase=project_phase,
                                                  progress_profitability=progress_profitability,
                                                  potential_problems=potential_problems,
                                                  )
            key_words = form.cleaned_data['key_words'].split(' ')
            new_project_form.save()
            for word in key_words:
                new_project_form.key_words.add(models.Keyword.objects.get_or_create(name=word)[0])
            # new_project = models.Project(project_form=new_project_form, industry_creator=request.user.industryuser)
            # new_project.save()
            return HttpResponseRedirect(reverse('industry:index'))
        return render(request, 'industry/newProject.html', context={'form': form})


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


class Messages(generic.TemplateView):
    template_name = 'industry/messages.html'
