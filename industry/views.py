from django.shortcuts import HttpResponseRedirect ,reverse ,get_object_or_404 ,render
from django.views import generic
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from . import forms ,models

class Index(generic.TemplateView):
    template_name = 'industry/index.html'
    industry = models.IndustryUser

    def get(self, request, *args, **kwargs):
        try:
            self.industry = get_object_or_404(models.IndustryUser ,user=request.user)
        except:
            return HttpResponseRedirect(reverse('chamran:login'))
        return super().get(request ,*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry'] = self.industry
        # context['MEDIA_URL'] = settings.MEDIA_URL
        try:
            if  self.industry.industryform:
                print(self.industry.industryform.name)
        except:
            context['basic_info'] = True
        return context
    
    def post(self ,request ,*args, **kwargs):
        form = forms.IndustryBasicInfoForm(request.POST ,request.FILES)
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
            # if email_address != request.user.email:
            #     raise ValidationError(_('پست الکترونیکی مطابقت ندارد.'))
            industry_info = models.IndustryForm(industry_user=request.user.industryuser,
                                                photo=photo,
                                                name=name ,
                                                registration_number =registration_number,
                                                date_of_foundation=date_of_foundation,
                                                research_field=research_field,
                                                industry_type=industry_type,
                                                industry_address =industry_address,
                                                phone_number=phone_number,
                                                email_address=email_address)
            industry_info.save()
        return HttpResponseRedirect(reverse('industry:index'))

class userInfo(generic.FormView):
    template_name = 'industry/userInfo.html'
    form_class = forms.IndustryInfoForm

    def post(self, request, *args, **kwargs):
        form = forms.IndustryInfoForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            registration_number = form.cleaned_data['registration_number']
            date_of_foundation = form.cleaned_data['date_of_foundation']
            research_field = form.cleaned_data['research_field']
            industry_type = form.cleaned_data['industry_type']
            industry_address = form.cleaned_data['industry_address']
            phone_number = form.cleaned_data['phone_number']
            email_address = form.cleaned_data['email_address']
            awards_honors = form.cleaned_data['awards_honors']
            tax_declaration = form.cleaned_data['tax_declaration']
           
            industry_form = models.IndustryForm(user = request.user ,name=name ,
            registration_number=registration_number , date_of_foundation=date_of_foundation ,
            research_field=research_field ,industry_type=industry_type ,
            industry_address=industry_address ,phone_number=phone_number ,
            email_address=email_address ,awards_honors=awards_honors , tax_declaration=tax_declaration)

            industry_form.save()
            return HttpResponseRedirect(reverse('industry:index'))
        return super().post(request, *args, **kwargs)


class newProject(generic.FormView):
    template_name = 'industry/newProject.html'
    form_class = forms.ProjectForm

    def post(self ,request ,*args, **kwargs):
        print(request.POST)
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            # 'required_technique'
            project_title_persian =  form.cleaned_data['project_title_persian']
            project_title_english =  form.cleaned_data['project_title_english']
            # key_words = form.cleaned_data['key_words']
            # research_methodology = form.cleaned_data['research_methodology']
            main_problem_and_importance = form.cleaned_data['main_problem_and_importance']
            predict_profit = form.cleaned_data['predict_profit']
            required_lab_equipment = form.cleaned_data['required_lab_equipment']
            innovation = form.cleaned_data['innovation']
            approach = form.cleaned_data['approach']
            policy = form.cleaned_data['policy']
            # required_budget = form.cleaned_data['required_budget']
            project_phase = form.cleaned_data['project_phase']
        
            new_project_form = models.ProjectForm(project_title_persian=project_title_persian,
                                             project_title_english=project_title_english,
                                            #  research_methodology=research_methodology,
                                             main_problem_and_importance=main_problem_and_importance,
                                             predict_profit=predict_profit,
                                             required_lab_equipment=required_lab_equipment,
                                             innovation=innovation,
                                             approach=approach,
                                             policy=policy,
                                            #  required_budget=required_budget,
                                             project_phase=project_phase,
                                             )
            new_project_form.save()
            new_project = models.Project(project_form=new_project_form ,industry_creator=request.user)
            return super().post(request ,args ,kwargs)
        return super().post(request ,args ,kwargs)