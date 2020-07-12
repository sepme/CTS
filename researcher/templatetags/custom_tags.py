from django import template
from chamran_admin.models import Message
from django.contrib.auth.models import User
from industry.models import Comment, Project
from researcher.models import ResearcherUser
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


@register.simple_tag()
def unseen_researcher_msgs(projectID, user):
    researcher = ResearcherUser.objects.get(user=User.objects.get(username=user))
    unseen_msgs = Comment.objects.filter(status="unseen", researcher_user=researcher,
                                         project=Project.objects.get(id=projectID)).all().count()
    return unseen_msgs
