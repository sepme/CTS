from django.views import generic
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, get_object_or_404
from .models import ExpertForm, EqTest, ExpertUser
from .forms import InitialInfoForm
from django.contrib.auth.decorators import login_required


class Index(generic.TemplateView):
    template_name = 'expert/index.html'


class UserInfo(generic.TemplateView):
    template_name = 'expert/userInfo.html'


class ResearcherRequest(generic.TemplateView):
    template_name = 'expert/researcherRequest.html'


class Messages(generic.TemplateView):
    template_name = 'expert/messages.html'


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
            expert_form = ExpertForm.objects.create(expert_firstname=first_name, expert_lastname=last_name, special_field=special_field, national_code=melli_code,
                                                    scientific_rank=scientific_rank, university=university, phone_number=home_number,home_address=address,
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


def test(request):
    return HttpResponse('Test view')




class Questions(generic.TemplateView):
    template_name = 'expert/questions.html'




























