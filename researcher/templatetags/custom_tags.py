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
    if researcher.status.status in 'not_answered':
        question = ResearchQuestionInstance.objects.filter(researcher=researcher).reverse().first()
        uniqe_id = question.research_question.uniqe_id
    else:
        uniqe_id = None
    return uniqe_id