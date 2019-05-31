from django.views import generic


class Index(generic.TemplateView):
    template_name = 'expert/base_profile.html'
