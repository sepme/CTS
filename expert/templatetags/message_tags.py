from django import template
from django.shortcuts import get_object_or_404

from industry.models import Project ,Comment
from chamran_admin.models import Message

register = template.Library()


@register.simple_tag
def getUnseenComments(project_id ,expert):
    project = get_object_or_404(Project ,pk=project_id)
    all_unseen = Comment.objects.filter(project=project).filter(status='unseen').filter(sender_type="industry")
    return all_unseen.filter(expert_user=expert).count()

@register.simple_tag
def getUnseenMessages(user):
    all_messages = Message.get_user_messages(user)
    return all_messages.exclude(read_by__in=[user]).count()