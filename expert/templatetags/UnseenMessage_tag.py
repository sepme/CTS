from django import template
from chamran_admin.models import Message

register = template.Library()

@register.simple_tag
def getUnseenMessages(user):
    all_messages = Message.get_user_messages(user)
    return all_messages.exclude(read_by__in=[user]).count()