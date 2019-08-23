from django.views import generic
from django.shortcuts import render
from .models import ExpertForm, EqTest
from .forms import InitialInfoForm

class Index(generic.TemplateView):
    template_name = 'expert/index.html'


class UserInfo(generic.TemplateView):
    template_name = 'expert/userInfo.html'


class ResearcherRequest(generic.TemplateView):
    template_name = 'expert/researcherRequest.html'


class Messages(generic.TemplateView):
    template_name = 'expert/messages.html'


def user_info(request):
    if request.method == 'POST':
        form = InitialInfoForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            special_field = form.cleaned_data['special_field']
            melli_code = form.cleaned_data['melli_code']
            scientific_rank = form.cleaned_data['scientific_rank']
            print(scientific_rank)
            university = form.cleaned_data['university']
            address = form.cleaned_data['address']
            home_number = form.cleaned_data['home_number']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            honors = form.cleaned_data['honors']
            team_work = form.cleaned_data['group-work']
            innovation = form.cleaned_data['creative-thinking']
            devotion = form.cleaned_data['sacrifice']
            productive_research = form.cleaned_data['researching']
            national_commitment = form.cleaned_data['obligation']
            collecting_information = form.cleaned_data['data-collection']
            business_thinking = form.cleaned_data['morale']
            risk_averse = form.cleaned_data['risk']
            method_of_introduction = form.cleaned_data['method_of_introduction']
            number_of_researcher = form.cleaned_data['student_num']
            has_industrial_research = form.cleaned_data['foreign_work']
            number_of_grants = form.cleaned_data['number_of_grants']

            expert_form = ExpertForm(expert_firstname=first_name, expert_lastname=last_name, special_field=special_field, national_code=melli_code, scientific_rank=scientific_rank,
                                     university=university, home_address=address, email_address=email,
                                     awards=honors, method_of_introduction=method_of_introduction, has_industrial_research=has_industrial_research)

            # eq_test = EqTest(team_work=team_work, innovation=innovation, devotion=devotion, productive_research=productive_research, national_commitment=national_commitment,
            #                 collecting_information=collecting_information, business_thinking=business_thinking, risk_averse=risk_averse)
            #
            # eq_test.save()
            # expert_form.eq_test = eq_test
            expert_form.save()

    return render(request, 'expert/userInfo.html', {})


def index(request):
    if request.method == 'POST':
        form = InitialInfoForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)

    else:
        form = InitialInfoForm()
    return render(request, 'expert/index.html', {'form': form})






























