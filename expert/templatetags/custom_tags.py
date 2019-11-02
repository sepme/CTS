from django import template
from persiantools.jdatetime import JalaliDate

register = template.Library()


@register.simple_tag
def calculate_date_past(date):
    diff = JalaliDate.today() - JalaliDate(date)
    days = diff.days
    if days < 0:
        return '0 روز'
    elif days < 7:
        return '{} روز'.format(days)
    elif days < 30:
        return '{} هفته'.format(int(days / 7))
    elif days < 365:
        return '{} ماه'.format(int(days / 30))
    else:
        return '{} سال'.format(int(days / 365))


@register.simple_tag
def calculate_date_remaining(date):
    diff = JalaliDate(date) - JalaliDate.today()
    days = diff.days
    if days < 0:
        return '0 روز'
    elif days < 7:
        return '{} روز'.format(days)
    elif days < 30:
        return '{} هفته'.format(int(days / 7))
    elif days < 365:
        return '{} ماه'.format(int(days / 30))
    else:
        return '{} سال'.format(int(days / 365))


@register.simple_tag
def calculate_deadline(finished, started):
    diff = JalaliDate(finished) - JalaliDate(started)
    days = diff.days
    if days < 0:
        return None
    elif days < 7:
        return '{} روز'.format(days)
    elif days < 30:
        return '{} هفته'.format(int(days / 7))
    elif days < 365:
        return '{} ماه'.format(int(days / 30))
    else:
        return '{} سال'.format(int(days / 365))
