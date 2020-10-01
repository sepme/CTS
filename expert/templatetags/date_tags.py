from django import template
from persiantools.jdatetime import JalaliDate
from industry.models import Project
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
def project_progress(project_pk):
    try:
        if Project.objects.filter(id=project_pk).exists():
            project = Project.objects.get(id=project_pk)
            if project.is_date_valid():
                total_days = (project.date_finished - project.date_project_started).total_seconds()
                pass_days = (datetime.date.today() - project.date_project_started).total_seconds()
                if total_days:
                    amount = 89 * pass_days / total_days
                    return str("{:.2f}".format(amount))
            return None
    except:
        return None


@register.simple_tag
def date_to_percent(project_pk, phase, type):
    return None
    # if Project.objects.filter(id=project_pk).exists():
    #     project = Project.objects.get(id=project_pk)
    #     if project.is_date_valid():
    #         if phase == 1:
    #             date = project.date_project_started
    #         elif phase == 2:
    #             date = project.date_phase_two_deadline
    #         elif phase == 3:
    #             date = project.finish_date_suggested
    #         else:
    #             date = ""
    #         total_days = (project.date_finished - project.date_project_started).total_seconds()
    #         pass_days = (date - project.date_project_started).total_seconds()
    #         if total_days:
    #             if type == "h":
    #                 return str(int((100 * pass_days / total_days) * 0.88 + 5))
    #             elif type == "w":
    #                 return str(int(81 * pass_days / total_days))
    #     return None


@register.simple_tag
def is_active(project_pk, phase):
    return ""
    # if Project.objects.filter(id=project_pk).exists() and phase is not None:
    #     project = Project.objects.get(id=project_pk)
    #     if project.is_date_valid():
    #         if phase == 1:
    #             date = project.date_project_started
    #         elif phase == 2:
    #             date = project.date_phase_two_deadline
    #         elif phase == 3:
    #             date = project.finish_date_suggested
    #         elif phase == 4:
    #             date = project.date_finished
    #         else:
    #             date = ""
    #         pass_days_from_now = (datetime.date.today() - project.date_project_started).total_seconds()
    #         pass_days = (date - project.date_project_started).total_seconds()
    #         delta = pass_days - pass_days_from_now
    #         if delta > 0:
    #             return ""
    #         return "active"
