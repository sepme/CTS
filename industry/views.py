from django.views import generic

class Index(generic.TemplateView):
    template_name = 'industry/index.html'
class userInfo(generic.TemplateView):
    template_name = 'industry/userInfo.html'
class newProject(generic.TemplateView):
    template_name = 'industry/newProject.html'
