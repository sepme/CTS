from django import template
from persiantools.jdatetime import JalaliDate

register = template.Library()


@register.filter
def gregorian_to_numeric_jalali(date):
    j_date = JalaliDate(date)
    return str(j_date.year) + ' ' + str(j_date.month) + ' ' + str(j_date.day)
