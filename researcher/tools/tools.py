from persiantools.jdatetime import JalaliDate, digits
from dateutil.relativedelta import relativedelta

from expert.models import ExpertUser
from industry.models import IndustryUser
from researcher.models import ResearcherUser
from researcher import persianNumber

def find_account_type(user):
    expert = ExpertUser.objects.filter(user=user)
    if expert.exists():
        return 'expert'
    industry = IndustryUser.objects.filter(user=user)
    if industry.exists():
        return 'industry'
    researcher = ResearcherUser.objects.filter(user=user)
    if researcher.exists():
        return 'researcher'
    else:
        return False


def find_user(user):
    if find_account_type(user) == 'expert':
        return user.expertuser
    elif find_account_type(user) == 'researcher':
        return user.researcheruser
    elif find_account_type(user) == 'industry':
        return user.industryuser
    else:
        return False

def gregorian_to_numeric_jalali(date):
    if date:
        j_date = JalaliDate(date)
        return digits.en_to_fa(str(j_date.year)) + '/' + digits.en_to_fa(str(j_date.month)) + '/' + digits.en_to_fa(str(j_date.day))
    else:
        return "نا مشخص"


def date_last(date1, date2):
    delta = relativedelta(date1, date2)
    days_passed = abs(delta.days)
    months_passed = abs(delta.months)
    years_passed = abs(delta.years)
    days = ""
    months = ""
    years = ""
    if years_passed != 0:
        years = persianNumber.convert(str(years_passed)) + " سال "
    if months_passed != 0:
        if years_passed != 0:
            months = " و " + persianNumber.convert(str(months_passed)) + " ماه "
        else:
            months = persianNumber.convert(str(months_passed)) + " ماه "
    if days_passed != 0:
        if months_passed == 0 and years_passed == 0:
            days = persianNumber.convert(str(days_passed)) + " روز "
        else:
            days = " و " + persianNumber.convert(str(days_passed)) + " روز "
    if days_passed != 0 or months_passed != 0 or years_passed != 0:
        return years + months + days
    return "امروز"
