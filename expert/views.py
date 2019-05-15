from django.shortcuts import render
from django.views import generic

class index(generic.TemplateView):
    template_name = 'expert/index.html'