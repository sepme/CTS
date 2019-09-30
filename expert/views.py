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


def user_info(request):
    instance = get_object_or_404(ExpertForm, expert_user__user=request.user)
    scientific_form = ScientificRecordForm()
    if request.method == 'POST':
        expert_info_form = ExpertInfoForm(request.POST or None, instance=instance)
        # scientific_form = ScientificRecordForm(request.POST or None)
        executive_form = ExecutiveRecordForm(request.POST or None)
        research_form = ResearchRecordForm(request.POST or None)
        paper_form = PaperRecordForm(request.POST or None)
        #
        # if expert_info_form.is_valid() and scientific_form.is_valid() and executive_form.is_valid() and research_form.is_valid() and paper_form.is_valid():
        #     expert_info_form.save()
        #     print("scientific form:", scientific_form.cleaned_data)
        #     print("executive form:", executive_form.cleaned_data)
        #     print("research form:", research_form.cleaned_data)
        #     print("paper form:", paper_form.cleaned_data)
        #     return HttpResponseRedirect(reverse('expert:test'))
    else:
        expert_info_form = ExpertInfoForm(instance=instance)
        # try:
        scientific_instance = ScientificRecord.objects.filter(expert_form=request.user.expertuser.expertform)
        # scientific_form = ScientificRecordForm(instance=scientific_instance)
        # except ScientificRecord.DoesNotExist():
        executive_form = ExecutiveRecordForm()
        research_form = ResearchRecordForm()
        print(request.user)
    return render(request, 'expert/userInfo.html', {'scientific_form': scientific_form,
                                                    'executive_form': executive_form,
                                                    'research_form': research_form,
                                                    'expert_info_form': expert_info_form,
                                                    'instance': instance,
                                                    'scientific_instance': scientific_instance})


def ajax_view(request):
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
