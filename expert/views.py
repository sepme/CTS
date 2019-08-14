from django.views import generic


class Index(generic.TemplateView):
    template_name = 'expert/index.html'


class UserInfo(generic.TemplateView):
    template_name = 'expert/userInfo.html'


class ResearcherRequest(generic.TemplateView):
    template_name = 'expert/researcherRequest.html'


class Messages(generic.TemplateView):
    template_name = 'expert/messages.html'
