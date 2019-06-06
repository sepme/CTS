from django.views import generic

class Index(generic.TemplateView):
    template_name = 'industry/base_profile.html'
