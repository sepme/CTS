from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.views import generic
from django.contrib.auth.models import User

from . import models


class Index(generic.TemplateView):
    template_name = 'researcher/index.html'


class Login(generic.TemplateView):
    template_name = 'registration/base.html'


class UserPass(generic.TemplateView):
    template_name = 'registration/user_pass.html'


def signup(request, username):
    print("-------------------")
    print("HEREEEEEEE IS RESEARCHER")
    user = get_object_or_404(User, username=username)
    researcher = models.ResearcherUser(user=user)
    researcher.save()
    return HttpResponseRedirect(reverse('researcher:index'))
