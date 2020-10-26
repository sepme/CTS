from django import template
from chamran_admin.models import Message
from django.templatetags.static import static
register = template.Library()


@register.simple_tag
def getUnseenMessages(user):
    all_messages = Message.get_user_messages(user)
    return all_messages.exclude(read_by__in=[user]).count()


@register.filter
def get_value_in_qs(queryset, key):
    return queryset.values(key, flat=True)


@register.filter
def get_detail_with_uuid(queryset, key):
    username = key
    fullname = ""
    photo = ""
    if queryset.get("industryUser").get("username") == key:
        fullname = queryset.get("industryUser").get("fullname")
        photo = queryset.get("industryUser").get("photo")
    else:
        for user in queryset.get("expertUsers"):
            if user.get("username") == key:
                fullname = user.get("fullname")
                photo = user.get("photo")
                break
        if fullname == "":
            for user in queryset.get("researcherUsers"):
                if user.get("username") == key:
                    fullname = user.get("fullname")
                    photo = user.get("photo")
                    break
    if photo is None:
        photo = static('industry/img/profile.jpg')
    return {
        "username": username,
        "fullname": fullname,
        "photo": photo
    }


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
