from django import template
from persiantools.jdatetime import JalaliDate
import datetime

register = template.Library()


@register.simple_tag
def calculate_date_past(date):
    if date is None:
        return "نامشخص"
    diff = JalaliDate.today() - JalaliDate(date)
    days = diff.days
    if days < 1:
        return 'چند لحظه'
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
    if date is None:
        return 'نامشخص'
    diff = JalaliDate(date) - JalaliDate.today()
    days = diff.days
    if days < 1:
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
    if finished is None or started is None:
        return 'نامشخص'
    diff = JalaliDate(finished) - JalaliDate(started)
    days = diff.days
    if days < 1:
        return None
    elif days < 7:
        return '{} روز'.format(days)
    elif days < 30:
        return '{} هفته'.format(int(days / 7))
    elif days < 365:
        return '{} ماه'.format(int(days / 30))
    else:
        return '{} سال'.format(int(days / 365))


@register.simple_tag
def gregorian_to_numeric_jalali(date):
    if date is None:
        return "نامشخص"
    j_date = JalaliDate(date)
    return str(j_date.year) + '/' + str(j_date.month) + '/' + str(j_date.day)


@register.simple_tag
def project_progress(project):
    total_days = (project.date_finished - project.date_project_started).total_seconds()
    pass_days = (datetime.date.today() - project.date_project_started).total_seconds()
    amount = 100 * pass_days / total_days
    if amount > 89:
        amount = 89
    return str("{:.2f}".format(amount))


@register.simple_tag
def date_to_percent(project, date):
    total_days = (project.date_finished - project.date_project_started).total_seconds()
    pass_days = (date - project.date_project_started).total_seconds()
    return str(int(100 * pass_days / total_days))


@register.simple_tag
def is_active(project, date):
    pass_days_from_now = (datetime.date.today() - project.date_project_started).total_seconds()
    pass_days = (date - project.date_project_started).total_seconds()
    delta = pass_days - pass_days_from_now
    if delta > 0:
        return ""
    return "active"
