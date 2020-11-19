from dateutil.relativedelta import relativedelta
from persiantools.jdatetime import JalaliDate, digits

from expert.models import ExpertUser
from industry.models import IndustryUser
from researcher.models import ResearcherUser

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


def JalaliToGregorianDate(date):
    datePart = date.split("/")
    return JalaliDate(year=int(datePart[0]), month=int(datePart[1]), day=int(datePart[2]))\
        .to_gregorian()

# function name says it all :)
def gregorian_to_numeric_jalali(date):
    if date:
        j_date = JalaliDate(date)
        return digits.en_to_fa(str(j_date.year)) + '/' + digits.en_to_fa(str(j_date.month)) + '/' + digits.en_to_fa(str(j_date.day))
    else:
        return "نا مشخص"


# returns the difference between the two dates. e.g. 3 ruz, 5 sal, ...
def date_dif(start_date, deadline_date):
    if start_date == None:
        return "نا مشخص"
    delta = relativedelta(deadline_date, start_date)
    if delta.years != 0:
        return str(delta.years) + ' سال'
    elif delta.months != 0:
        return str(delta.months) + ' ماه'
    elif delta.days != 0:
        return str(delta.days) + ' روز'
    else:
        return 'امروز'

