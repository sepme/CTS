from django import template
from chamran_admin.models import Message
from researcher.models import ResearchQuestionInstance

register = template.Library()

@register.simple_tag
def getUnseenMessages(user):
    all_messages = Message.get_user_messages(user)
    return all_messages.exclude(read_by__in=[user]).count()

@register.simple_tag
def getQuestionUrl(researcher):
    uniqe_id = None
    if researcher.status.status in 'not_answered':
        question = ResearchQuestionInstance.objects.filter(researcher=researcher).reverse().first()        
        if question is not None:
            uniqe_id = question.research_question.uniqe_id
    return uniqe_id