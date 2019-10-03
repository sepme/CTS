from django.views import generic
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, get_object_or_404
from .models import ExpertForm, EqTest, ExpertUser
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, QueryDict


class Index(generic.TemplateView):
    template_name = 'expert/index.html'


class ResearcherRequest(generic.TemplateView):
    template_name = 'expert/researcherRequest.html'


class Messages(generic.TemplateView):
    template_name = 'expert/messages.html'


class Questions(generic.TemplateView):
    template_name = 'expert/questions.html'


@login_required(login_url='/login/')
def index(request):
    expert_user = get_object_or_404(ExpertUser, user=request.user)
    if request.method == 'POST':
        form = InitialInfoForm(request.POST, request.FILES)
        print(form.is_valid())

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            special_field = form.cleaned_data['special_field']
            melli_code = form.cleaned_data['melli_code']
            scientific_rank = form.cleaned_data['scientific_rank']
            university = form.cleaned_data['university']
            address = form.cleaned_data['address']
            home_number = form.cleaned_data['home_number']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email_address']
            expert_form = ExpertForm.objects.create(expert_firstname=first_name, expert_lastname=last_name,
                                                    special_field=special_field, national_code=melli_code,
                                                    scientific_rank=scientific_rank, university=university,
                                                    phone_number=home_number, home_address=address,
                                                    mobile_phone=phone_number, email_address=email)
            expert_form.expert_user = expert_user
            if request.FILES.get('photo'):
                photo = request.FILES.get('photo')
                expert_form.photo.save(photo.name, photo)
            expert_user.status = 'free'
            expert_user.save()
            expert_form.save()
            return HttpResponseRedirect(reverse('expert:index'))

    else:
        form = InitialInfoForm()
    return render(request, 'expert/index.html', {'form': form, 'expert_user': expert_user})


# def user_info(request):
#     instance = get_object_or_404(ExpertForm, expert_user__user=request.user)
#     expert_form = request.user.expertuser.expertform
#     scientific_instance = ScientificRecord.objects.filter(expert_form=expert_form)
#     executive_instance = ExecutiveRecord.objects.filter(expert_form=expert_form)
#     research_instance = ResearchRecord.objects.filter(expert_form=expert_form)
#     paper_instance = PaperRecord.objects.filter(expert_form=expert_form)
#     if request.method == 'POST':
#         print(request.POST)
#         eq_test_form = EQTestForm(request.POST)
#         expert_info_form = ExpertInfoForm(request.POST or None, instance=instance)
#         team_work = request.POST['team_work']
#         creative_thinking = request.POST['creative-thinking']
#         sacrifice = request.POST['sacrifice']
#         researching = request.POST['researching']
#         obligation = request.POST['obligation']
#         data_collection = request.POST['data-collection']
#         morale = request.POST['morale']
#         risk = request.POST['risk']
#
#         # if expert_info_form.is_valid() and scientific_form.is_valid() and executive_form.is_valid() and research_form.is_valid() and paper_form.is_valid():
#         #     expert_info_form.save()
#         #     print("scientific form:", scientific_form.cleaned_data)
#         #     print("executive form:", executive_form.cleaned_data)
#         #     print("research form:", research_form.cleaned_data)
#         #     print("paper form:", paper_form.cleaned_data)
#         #     return HttpResponseRedirect(reverse('expert:test'))
#     else:
#         eq_test_form = EQTestForm()
#         expert_info_form = ExpertInfoForm(instance=instance)
#         print(request.user)
#     return render(request, 'expert/userInfo.html', {'scientific_form': ScientificRecordForm(),
#                                                     'executive_form': ExecutiveRecordForm(),
#                                                     'research_form': ResearchRecordForm(),
#                                                     'paper_form': PaperRecordForm(),
#                                                     'eq_test_form': eq_test_form,
#                                                     'expert_info_form': expert_info_form,
#                                                     'scientific_instance': scientific_instance,
#                                                     'executive_instance': executive_instance,
#                                                     'research_instance': research_instance,
#                                                     'paper_instance': paper_instance})


class UserInfo(generic.FormView):
    template_name = 'expert/userInfo.html'
    form_class = ExpertInfoForm

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(ExpertForm, expert_user__user=request.user)
        expert_info_form = ExpertInfoForm(instance=instance)
        scientific_instance = ScientificRecord.objects.filter(expert_form=instance)
        executive_instance = ExecutiveRecord.objects.filter(expert_form=instance)
        research_instance = ResearchRecord.objects.filter(expert_form=instance)
        paper_instance = PaperRecord.objects.filter(expert_form=instance)
        context = {'expert_info_form': expert_info_form,
                   'scientific_instance': scientific_instance,
                   'executive_instance': executive_instance,
                   'research_instance': research_instance,
                   'paper_instance': paper_instance,
                   'expert_form': instance,
                   'scientific_form': ScientificRecordForm(),
                   'executive_form': ExecutiveRecordForm(),
                   'research_form': ResearchRecordForm(),
                   'paper_form': PaperRecordForm()
                   }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        instance = get_object_or_404(ExpertForm, expert_user__user=request.user)
        expert_info_form = ExpertInfoForm(request.POST, request.FILES, instance=instance)
        team_work = request.POST.get('team_work', False)
        creative_thinking = request.POST.get('creative-thinking', False)
        sacrifice = request.POST.get('sacrifice', False)
        researching = request.POST.get('researching', False)
        obligation = request.POST.get('obligation', False)
        data_collection = request.POST.get('data-collection', False)
        morale = request.POST.get('morale', False)
        risk = request.POST.get('risk', False)
        student_num = request.POST.get('student_num', False)
        foreign_work = request.POST.get('foreign_work', False)
        scientific_instance = ScientificRecord.objects.filter(expert_form=instance)
        executive_instance = ExecutiveRecord.objects.filter(expert_form=instance)
        research_instance = ResearchRecord.objects.filter(expert_form=instance)
        paper_instance = PaperRecord.objects.filter(expert_form=instance)
        context = {'expert_info_form': expert_info_form,
                   'scientific_instance': scientific_instance,
                   'executive_instance': executive_instance,
                   'research_instance': research_instance,
                   'paper_instance': paper_instance,
                   'expert_form': instance,
                   'scientific_form': ScientificRecordForm(),
                   'executive_form': ExecutiveRecordForm(),
                   'research_form': ResearchRecordForm(),
                   'paper_form': PaperRecordForm()
                   }
        if expert_info_form.is_valid():
            expert_form = expert_info_form.save(commit=False)
            expert_form.expert_user = request.user.expertuser
            if team_work and creative_thinking and sacrifice and researching and obligation and data_collection and morale and risk:
                if instance.eq_test:
                    eq_test = instance.eq_test
                else:
                    eq_test = EqTest()
                eq_test.team_work = team_work
                eq_test.innovation = creative_thinking
                eq_test.devotion = sacrifice
                eq_test.productive_research = researching
                eq_test.national_commitment = obligation
                eq_test.collecting_information = data_collection
                eq_test.business_thinking = morale
                eq_test.risk_averse = risk
                eq_test.save()
                expert_form.eq_test = eq_test
            if foreign_work and student_num:
                print('2 variables initiated')
                expert_form.has_industrial_research = foreign_work
                expert_form.number_of_researcher = student_num

            if request.FILES.get('photo'):
                photo = request.FILES.get('photo')
                expert_form.photo.save(photo.name, photo)
            expert_form.save()
            return HttpResponseRedirect(reverse('expert:index'))

        return render(request, self.template_name, context)


def scienfic_record_view(request):
    print(request.is_ajax())
    # form = request.GET.get('formData', None)
    # print(form)
    print(request.POST)
    scientific_form = ScientificRecordForm(request.POST)
    if scientific_form.is_valid():
        print(scientific_form.cleaned_data)
        data = {'success': 'successful'}
        scientific_record = scientific_form.save(commit=False)
        scientific_record.expert_form = request.user.expertuser.expertform
        scientific_record.save()
        return JsonResponse(data)
    else:
        print('form error occured')
        return JsonResponse(scientific_form.errors)


def executive_record_view(request):
    executive_form = ExecutiveRecordForm(request.POST)
    if executive_form.is_valid():
        print(executive_form.cleaned_data)
        data = {'success': 'successful'}
        executive_record = executive_form.save(commit=False)
        executive_record.expert_form = request.user.expertuser.expertform
        executive_record.save()
        return JsonResponse(data)
    else:
        print('form error occured')
        return JsonResponse(executive_form.errors)


def research_record_view(request):
    research_form = ResearchRecordForm(request.POST)
    if research_form.is_valid():
        print(research_form.cleaned_data)
        data = {'success': 'successful'}
        research_record = research_form.save(commit=False)
        research_record.expert_form = request.user.expertuser.expertform
        research_record.save()
        return JsonResponse(data)
    else:
        print('form error occured')
        return JsonResponse(research_form.errors)


def paper_record_view(request):
    paper_form = PaperRecordForm(request.POST)
    if paper_form.is_valid():
        print(paper_form.cleaned_data)
        data = {'success': 'successful'}
        paper_record = paper_form.save(commit=False)
        paper_record.expert_form = request.user.expertuser.expertform
        paper_record.save()
        return JsonResponse(data)
    else:
        print('form error occured')
        return JsonResponse(paper_form.errors)
