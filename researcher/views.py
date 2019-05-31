from django.views import generic


class Index(generic.TemplateView):
    template_name = 'researcher/base_profile.html'
