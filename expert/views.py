from django.views import generic


class Index(generic.TemplateView):
    template_name = 'expert/index.html'
class userInfo(generic.TemplateView):
        template_name = 'expert/userInfo.html'